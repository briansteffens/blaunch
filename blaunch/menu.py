import os
import sys
import wx

class Node:
    shortcut = None
    description = None

    parent = None
    children = []

    command = None
    working_directory = None

    def __init__(self):
        self.children = []

    def Path(self):
        """Return the full path to this Node

        Recursively prepends ancestors' shortcuts to this Node's shortcut.
        Given a hierarchy like: [root] -> [folders] -> [home],
        [home].path() would return "foldershome".
        """

        if self.parent is None: # This must be the root node. Start the chain.
            return '';

        return self.parent.Path() + self.shortcut

    def Resolve(self, path):
        """Return a descendant Node

        Recursively searches children looking for a complete match to [path].
        Given a hierarchy like: [root] -> [folders] -> [home],
        [root].resolve('foldershome') would return [home].
        """

        # Try the first character of the path, then the first and second
        # characters, and so on.
        for match_len in range(1, len(path) + 1):
            match = path[:match_len]

            for child in self.children:
                if child.shortcut != match: # It's not a match.
                    continue

                if match_len >= len(path): # It matches the entire path.
                    return child

                # We found a match but not against the entire path. Take the
                # remaining part of the path and continue recursion on it.
                return child.Resolve(path[match_len:])

        raise LookupError(path + ' could not be resolved.')

    def Match(self, path):
        """Return all possible matches for [path].

        Given a hierarchy like: [root] -> [level1] -> [level2] -> [level3]..

        A path of 'level1' would return [level2] and any direct siblings.

        A path of 'level1level' would return [level2] and any direct siblings
        that start with 'level'. Neither example would return [level1] or
        [level3].
        """

        # Empty path: return all children.
        if path == '':
            return self.children

        # Try to go deeper into the hierarchy if possible.
        for child in self.children:
            # Exact match. Return it, or if it has children, return them.
            if path == child.shortcut:
                if len(child.children) == 0:
                    return [child]
                else:
                    return child.children

            # Partial match. Continue recursion.
            if path.startswith(child.shortcut):
                return child.Match(path[len(child.shortcut):])

        # Can't go any deeper. Check for partial matches on this level.
        partial_matches = []

        for child in self.children:
            if child.shortcut.startswith(path):
                partial_matches.append(child)

        return partial_matches

    @staticmethod
    def Load(file_contents):
        """Return a root node with loaded hierarchy from a config file
        """

        dictionaries = Node._Parse(file_contents)
        nodes = Node._Generate_Nodes(dictionaries)
        root = Node._Link(nodes)

        return root

    @staticmethod
    def _Parse(file_contents):
        """Return a list of dictionaries extracted from [file_contents].

        Given a [file_contents] of:
            key=val

            key=val2
            other=val3

        Returns:
            [
                {
                    key: val
                },
                {
                    key: val2,
                    other: val3
                }
            ]
        """

        dictionaries = []
        dictionary = {}

        for line in file_contents.splitlines():
            line = line.strip()

            if line.lower().startswith('shortcut'):
                if len(dictionary) > 0:
                    dictionaries.append(dictionary)

                dictionary = {}

            parts = line.split('=', 1)

            if len(parts) < 2:
                continue

            key = parts[0].strip().lower()
            val = parts[1].strip()

            dictionary[key] = val

        if len(dictionary) > 0:
            dictionaries.append(dictionary)

        return dictionaries

    @staticmethod
    def _Generate_Nodes(dictionaries):
        """Return a list of Nodes from the provided list of dictionaries.

        Each dictionary in [dictionaries] represents a Node. Key/value pairs in
        a dictionary represent attributes and values in the resultant Node.

        Linking is not done here. Node.children will be an empty list and
        Node.parent will a string path referencing the parent.
        """

        nodes = []

        for dictionary in dictionaries:
            node = Node()

            node.shortcut = dictionary['shortcut']

            if 'description' in dictionary:
                node.description = dictionary['description']

            if 'parent' in dictionary:
                node.parent = dictionary['parent']

            if 'command' in dictionary:
                node.command = dictionary['command']

            if 'working_directory' in dictionary:
                node.working_directory = dictionary['working_directory']

            nodes.append(node)

        return nodes


    @staticmethod
    def _Link(nodes):
        """Return a root node with a linked hierarchy.

        Given a list of Node instances, this performs linking based on values
        in Node.parent. Nodes without parents will be treated as children of
        root.
        """

        root = Node()
        root.shortcut = 'root'
        root.description = 'root'

        for node in nodes:
            if node.parent is None:
                node.parent = root
            else:
                node.parent = root.Resolve(node.parent)
                if node.parent is None:
                    print 'error 12345: ' + node.shortcut
                    return None

            node.parent.children.append(node)

        return root
