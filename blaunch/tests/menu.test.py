import sys
import os

import unittest

sys.path.append(os.path.abspath('../'))
from menu import Node

class NodeTests(unittest.TestCase):

	def setUp(self):
		"""Before each test case"""
		
	def tearDown(self):
		"""After each test case"""
		
		
	def test_Path(self):
		"""Node.Path() should return all of the Node's ancestors' shortcuts 
		(except the root Node) concatenated.
		
		"""
		
		root = Node()
		
		child = Node()
		child.shortcut = 'child'
		child.parent = root
		root.children.append(child)
		
		descendant = Node()
		descendant.shortcut = 'descendant'
		descendant.parent = child
		child.children.append(descendant)
		
		
		self.assertEquals(root.Path(), '', '[root].Path() should return "".')
		
		self.assertEquals(child.Path(), 'child', 
			'[child].Path() should return "child".')
			
		self.assertEquals(descendant.Path(), 'childdescendant',
			'[descendant].Path() should return "childdescendant".')
		
		
	def test_Resolve(self):
		""" Node.Resolve(path) should take a path and return the sub-Node it
		references.
		
		"""
		
		root = Node()
		child = Node()
		descendant = Node()
		noise = Node() # An extra node to make sure selection is working.
		
		child.shortcut = 'ch'
		root.children.append(child)
		child.parent = root
		
		noise.shortcut = 'ch not used' # Make sure it doesn't match this,
		root.children.append(noise)
		noise.parent = root
		
		descendant.shortcut = 'desc'
		child.children.append(descendant)
		descendant.parent = child
		
		
		# Should get an error if looking for a sub-Node that doesn't exist
		self.assertRaises(LookupError, root.Resolve, 'not valid')
		
		# Return a child of root (no recursion)
		self.assertEquals(root.Resolve('ch'), child, 
			'Not finding a child Node.')
		
		# Return a descendant of root (recursion)
		self.assertEquals(root.Resolve('chdesc'), descendant,
			'Not finding a descendant Node.')
	
	
	def test_Match(self):
		"""Node.Match(path) should return all possible matches to path within
		[path].children or [path].parent.children.
		
		"""
	
		root = Node()

		child = Node()
		child.shortcut = 'ch1'
		child.parent = root
		root.children.append(child)
		
		descendant = Node()
		descendant.shortcut = 'd1'
		descendant.parent = child
		child.children.append(descendant)
		
		descendant2 = Node()
		descendant2.shortcut = 'd2'
		descendant2.parent = child
		child.children.append(descendant2)
		
		child2 = Node()
		child2.shortcut = 'other'
		child2.parent = root
		root.children.append(child2)
		
		
		# An empty string should return all immediate children of [root].
		target = root.Match('')
		self.assertEquals(len(target), 2, 'Expected 2 results.')
		self.assertEquals(target[0], child, 'Expected [child].')
		self.assertEquals(target[1], child2, 'Expected [child2].')
		
		# "ch" should return only "ch1".
		target = root.Match('ch')
		self.assertEquals(len(target), 1, 'Expected 1 result.')
		self.assertEquals(target[0], child, 'Expected [child].')
		
		# "ch1" should return all immediate children of [child].
		target = root.Match('ch1')
		self.assertEquals(len(target), 2, 'Expected 2 results.')
		self.assertEquals(target[0], descendant, 'Expected [descendant].')
		self.assertEquals(target[1], descendant2, 'Expected [descendant2].')
		
		# "ch1d" should return both immediate children of [child].
		target = root.Match('ch1d')
		self.assertEquals(len(target), 2, 'Expected 2 results.')
		self.assertEquals(target[0], descendant, 'Expected [descendant].')
		self.assertEquals(target[1], descendant2, 'Expected [descendant2].')

		# "ch1d2" should return [descendant2].
		target = root.Match('ch1d2')
		self.assertEquals(len(target), 1, 'Expected 1 result.')
		self.assertEquals(target[0], descendant2, 'Expected [descendant2].')

		# "ch1d3" should return [].
		target = root.Match('ch1d3')
		self.assertEquals(len(target), 0)
		
		# "otherfake" should return [].
		target = root.Match('otherfake')
		self.assertEquals(len(target), 0)
	
			
	def test_Load(self):
		"""Tests Node.Load().
		
		This is kind of an integration test, as load() is currently just a
		wrapper around 3 "private" methods. See below for direct tests on them.
		
		"""

		# Given..
		file_contents = \
			'Shortcut=child\nShortcut=descendant\nParent=child'

		# When..
		root = Node.Load(file_contents)
		
		# Then..	[This is just a copy from test_link]
		self.assertEquals(len(root.children), 1, 
			'Expected 1 child of [root].')

		self.assertEquals(len(root.children[0].children), 1, 
			'Expected 1 child of [child].')
			
		self.assertEquals(len(root.children[0].children[0].children), 0,
			'Expected 0 children of [descendant].')
			
		self.assertTrue(root.parent is None,
			'Expected the parent of [root] to be None.')
			
		self.assertEquals(root.children[0].parent, root,
			'Expected the parent of [child] to be [root].')
			
		self.assertEquals(root.children[0].children[0].parent, 
			root.children[0],
			'Expected the parent of [descendant] to be [child].')
			
			
	def test_Parse(self):

		# Given..
		file_contents = \
			'Shortcut=10 \n\tval=ten\r\nShortcut=15\t\rval=fifteen '
		
		# When..
		result = Node._Parse(file_contents)

		# Then..
		self.assertEquals(len(result), 2, 
			'Not detecting empty line borders between nodes properly.')
			
		self.assertEquals(len(result[0]), 2,
			'Wrong number of key/value pairs in the first node.')
						
		self.assertEquals(result[0]['shortcut'], '10',
			'Failed to parse the first key/value pair of the first node.')
			
		self.assertEquals(result[0]['val'], 'ten',
			'Failed to parse the second key/value pair of the first node.')

		self.assertEquals(len(result[1]), 2,
			'Wrong number of key/value pairs in the second node.')
			
		self.assertEquals(result[1]['shortcut'], '15',
			'Failed to parse the first key/value pair of the second node.')
			
		self.assertEquals(result[1]['val'], 'fifteen',
			'Failed to parse the second key/value pair of the second node.')
			

	def test_Generate_Nodes(self):
		
		# Given..
		dictionaries = []
		dictionaries.append({})
		dictionaries[0]['shortcut'] = 'child'
		dictionaries[0]['description'] = 'child description'
		
		dictionaries.append({})
		dictionaries[1]['shortcut'] = 'descendant'
		dictionaries[1]['parent'] = 'child'
		dictionaries[1]['working_directory'] = 'working dir'

		# When..
		result = Node._Generate_Nodes(dictionaries)
		
		# Then..
		self.assertEquals(len(result), 2, 'Expected 2 results.')
		
		self.assertEquals(result[0].shortcut, 'child',
			'Expected result0.shortcut to be "child".')
		self.assertTrue(result[0].parent is None,
			'Expected result0.parent to be None.')			
		self.assertEquals(len(result[0].children), 0,
			'Expected result0.children to be empty.')
		self.assertEquals(result[0].description, 'child description',
			'Expected result0.description to be "child description".')
		self.assertIsNone(result[0].working_directory,
			'Expected result0.working_directory to be None.')
		
		self.assertEquals(result[1].shortcut, 'descendant',
			'Expected result1.shortcut to be "descendant".')
		self.assertEquals(result[1].parent, 'child',
			'Expected result1.parent to be "child".')			
		self.assertEquals(len(result[1].children), 0,
			'Expected result1.children to be empty.')
		self.assertTrue(result[1].description is None,
			'Expected result1.description to be None.')
		self.assertEquals(result[1].working_directory, 'working dir',
			'Expected result1.working_directory to be "working_dir".')
		
	
	def test_Link(self):
	
		# Given..
		nodes = []
		nodes.append(Node())
		nodes.append(Node())
		
		nodes[0].shortcut = 'child'
		
		nodes[1].shortcut = 'descendant'
		nodes[1].parent = 'child'
		
		# When..
		root = Node._Link(nodes)
		
		# Then..
		self.assertEquals(len(root.children), 1, 
			'Expected 1 child of [root].')

		self.assertEquals(len(root.children[0].children), 1, 
			'Expected 1 child of [child].')
			
		self.assertEquals(len(root.children[0].children[0].children), 0,
			'Expected 0 children of [descendant].')
			
		self.assertTrue(root.parent is None,
			'Expected the parent of [root] to be None.')
			
		self.assertEquals(root.children[0].parent, root,
			'Expected the parent of [child] to be [root].')
			
		self.assertEquals(root.children[0].children[0].parent, 
			root.children[0],
			'Expected the parent of [descendant] to be [child].')
		

if __name__ == "__main__":
	unittest.main()
	
	
	
	
	
	
	
	
	
	
	
