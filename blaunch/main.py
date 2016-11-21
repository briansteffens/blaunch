import os
import sys
import subprocess
import math
import wx
import wx.lib.scrolledpanel as scrolled

from menu import Node
from conf import Config

class MainFrame(wx.Frame):
    config = None
    root = None
    panel = None
    scroll = None
    scroll_vbox = None
    input_text = None
    output = None
    nodes = []
    output_items = []
    output_width_characters = -1

    def __init__(self, parent, root_node, config, id):
        self.config = config

        wx.Frame.__init__(self, parent, id, 'blaunch', self.config.position,
                self.config.size)

        self.root = root_node
        self.SetFont(wx.Font(self.config.font_size, wx.MODERN, wx.NORMAL,
            wx.NORMAL, False, self.config.font_name))

        self.panel = wx.Panel(self)
        panel_vbox = wx.BoxSizer(wx.VERTICAL)

        self.input_text = wx.TextCtrl(self.panel)
        panel_vbox.Add(self.input_text, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT,
                self.config.padding)
        self.input_text.Bind(wx.EVT_KEY_UP, self.OnKeyPress)
        self.input_text.SetFocus()

        self.scroll = scrolled.ScrolledPanel(self.panel, -1)
        self.scroll.Bind(wx.EVT_SIZE, self.on_scroll_size)
        self.scroll_vbox = wx.BoxSizer(wx.VERTICAL)

        self.scroll.SetSizer(self.scroll_vbox)
        self.scroll.SetAutoLayout(1)
        self.scroll.SetupScrolling()

        panel_vbox.Add(self.scroll, 1, wx.EXPAND|wx.ALL, self.config.padding)
        self.panel.SetSizer(panel_vbox)
        self.panel.SetAutoLayout(1)

    def is_shell_command(self):
        return self.input_text.GetValue().startswith(self.config.shell_prefix)

    def OnKeyPress(self, event):
        if event.GetKeyCode() == 27:
            self.Close()

        enter = event.GetKeyCode() == 13

        if self.is_shell_command() and enter:
            self.process_shell_command(self.input_text.GetValue())
            return

        self.update_output()

        if len(self.nodes) == 1 and \
                self.nodes[0].path() == self.input_text.GetValue():
            if self.config.auto_run or enter:
                self.process(self.nodes[0])
                return

        event.Skip()

    def process(self, node):
        if node.command is None:
            return

        process = subprocess.Popen(node.command.split(),
            stdout=subprocess.PIPE,cwd=node.working_directory)

        self.Close()

    def process_shell_command(self, command):
        command = command.replace(self.config.shell_prefix, "").strip()

        subprocess.Popen(command, shell=True)

        self.Close()

    def on_scroll_size(self, event):
        self.output_width_characters = int(math.floor(self.GetClientSize()[0] /
            self.GetTextExtent(' ')[0])) - 3
        self.update_output()

    def update_output(self):
        for item in self.output_items:
            self.scroll.RemoveChild(item)
            item.Destroy()
        self.output_items = []

        # If the command matches the shell prefix. Ex: "$ hydrogen"
        if self.is_shell_command():
            item = wx.StaticText(self.scroll, -1, "Enter a shell command..")
            self.scroll_vbox.Add(item, 0, wx.ALIGN_CENTER|wx.LEFT|wx.RIGHT,
                    self.config.padding)
            self.output_items.append(item)
        # Otherwise it's a normal shortcut from menu.conf
        else:
            self.nodes = self.root.match(self.input_text.GetValue())
            for node in self.nodes:
                label = self.overlay_strings(node.shortcut, node.description,
                        self.output_width_characters)
                item = wx.StaticText(self.scroll, -1, label)
                self.scroll_vbox.Add(item, 0, wx.ALIGN_LEFT|wx.LEFT|wx.RIGHT,
                        self.config.padding)
                self.output_items.append(item)

        self.scroll.Layout()

    def overlay_strings(self, left, right, length):
        if left is None: left = ''
        if right is None: right = ''

        result = left

        overlap = (len(left) + len(right)) - length

        if overlap < 0:
            for i in range(overlap, 0):
                result += ' '
            overlap = 0

        result += right[overlap:]

        if len(result) > length:
            result = result[:length]

        return result

    @staticmethod
    def run_launcher():
        app = wx.PySimpleApp()

        config_contents = open('/etc/blaunch/blaunch.conf', 'r').read()
        config = Config(config_contents)

        menu_contents = open('/etc/blaunch/menu.conf', 'r').read()
        root_node = Node.load(menu_contents)

        frame = MainFrame(parent = None, root_node = root_node,
                config = config, id = -1)
        frame.Show()
        app.MainLoop()


if __name__ == '__main__':
    MainFrame.run_launcher()
