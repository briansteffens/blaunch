import sys
import os

import wx

import unittest

sys.path.append(os.path.abspath('../'))
from main import MainFrame
from conf import Config

class MainFrameTests(unittest.TestCase):

	target = None

	def setUp(self):
		"""Before each test case"""
		app = wx.PySimpleApp()
		self.target = MainFrame(parent = None, root_node = None, config = Config(None), id = -1)		

		
	def tearDown(self):
		"""After each test case"""
		
		
	def test_OverlayStrings(self):
		self.assertEquals(self.target.OverlayStrings('', '', 4), '    ', 'Expected 4 spaces.')
		self.assertEquals(self.target.OverlayStrings('ab', 'cd', 4), 'abcd', 'Expected "abcd".')
		self.assertEquals(self.target.OverlayStrings('ab', 'cd', 5), 'ab cd', 'Expected "ab cd".')
		self.assertEquals(self.target.OverlayStrings('abc', 'def', 4), 'abcf', 'Expected "abcf".')
		self.assertEquals(self.target.OverlayStrings('ab', 'cd', 1), 'a', 'Expected "a".')
		self.assertEquals(self.target.OverlayStrings('ab', None, 3), 'ab ', 'Expected "ab ".')
		self.assertEquals(self.target.OverlayStrings(None, 'cd', 3), ' cd', 'Expected " cd".')
		

if __name__ == "__main__":
	unittest.main()
	
	
	
	
	
	
	
	
	
	
	
