import sys
import os

import unittest

sys.path.append(os.path.abspath('../'))
from conf import Config

class ConfigTests(unittest.TestCase):

    def setUp(self):
        """Before each test case"""
        
    def tearDown(self):
        """After each test case"""
        
        
    def test_Init(self):
        # We should get sane default values even if the config data passed in is None.
        self.init_defaults(Config(None))
        
        # We should get sane default values even with an empty config data string.
        self.init_defaults(Config(''))
        
        # Setting various parameters should change those values, leaving others as defaults.
        target = Config('auto_run=True\npadding=20\nposition_x=200')
        self.assertEquals(target.auto_run, True, 'Expected True for custom auto_run.') # Custom
        self.assertEquals(target.padding, 20, 'Expected 20 for custom padding.') # Custom
        self.assertEquals(target.font_size, 10, 'Expected 10 for default font_size.') # Default
        self.assertEquals(target.font_name, U'Monospace', 'Expected U"Monospace" for default font_name.') # Default
        self.assertEquals(target.position, (200, 400), 'Expected (200, 400) for custom position.') # Mix
        self.assertEquals(target.size, (300, 250), 'Expected (300, 250) for default size.') # Default
        self.assertEquals(target.shell_prefix, U'$', 'Expected U"$" for default shell_prefix.') # Default

        # Test auto_run
        self.assertEquals(Config('auto_run=True').auto_run, True, 'Expected True for custom auto_run.')
        self.assertEquals(Config('auto_run=true').auto_run, True, 'Case incensitivity test failed for auto_run.')
        self.assertEquals(Config('auto_run=False').auto_run, False, 'Expected False for custom auto_run.')
        
        # Test padding
        self.assertEquals(Config('padding=30').padding, 30, 'Expected 30 for custom padding.')
        self.assertEquals(Config('padding= 30 ').padding, 30, 'Spaces are not being trimmed from config data?')
        
        # Test font_size
        self.assertEquals(Config('font_size=15').font_size, 15, 'Expected 15 for custom font_size.')
        
        # Test font_name
        self.assertEquals(Config('font_name=SomeOtherFont').font_name, U'SomeOtherFont', 'Expected "SomeOtherFont".')
        
        # Test position_x
        self.assertEquals(Config('position_x=10').position, (10, 400), 'Expected (10, 400) for position.')
        
        # Test position_y
        self.assertEquals(Config('position_y=15').position, (810, 15), 'Expected (810, 15) for position.')
        
        # Test size_w
        self.assertEquals(Config('size_w=20').size, (20, 250), 'Expected (20, 250) for size.')
        
        # Test size h
        self.assertEquals(Config('size_h=25').size, (300, 25), 'Expected (300, 25) for size.')
        
        # Test shell_prefix
        self.assertEquals(Config('shell_prefix=$').shell_prefix, U'$', 'Expected "$".')


    def init_defaults(self, target):
        self.assertEquals(target.auto_run, False, 'Expected False for default auto_run.')
        self.assertEquals(target.padding, 5, 'Expected 5 for default padding.')
        self.assertEquals(target.font_size, 10, 'Expected 10 for default font_size.')
        self.assertEquals(target.font_name, U'Monospace', 'Expected U"Monospace" for default font_name.')
        self.assertEquals(target.position, (810, 400), 'Expected (810, 400) for default position.')
        self.assertEquals(target.size, (300, 250), 'Expected (300, 250) for default size.') 
        self.assertEquals(target.shell_prefix, U'$', 'Expected U"$" for default shell_prefix.')
        

    def test_Parse(self):
        # Test input data of None.
        target = Config._Parse(None)
        self.assertEquals(len(target), 0, 'Input data of None is not working.')
        
        # Test input data of empty string.
        target = Config._Parse('')
        self.assertEquals(len(target), 0, 'Input data of empty string is not working.')
        
        # Test basic key-value pair.
        target = Config._Parse('left=right')
        self.assertEquals(len(target), 1, 'Basic key-value pair is not being read properly. Expected 1 result.')
        self.assertEquals(target['left'], 'right', 
            'Basic key-value pair is not being read properly. Expected "left" = "right".')
        
        # Test key and value whitespace trimming.
        target = Config._Parse(' le ft  =\tright  \t ')
        self.assertEquals(len(target), 1, 'Key-value pair whitespace trimming is not working. Expected 1 result.')
        self.assertEquals(target['le ft'], 'right', 
            'Key-value pair whitespace trimming is not working. Expected "le ft" = "right".')
    
        # Test multiple key-value pairs.
        target = Config._Parse('first=value1\nsecond=value2')
        self.assertEquals(len(target), 2, 'Multiple key-value pairs are not working. Expected 2 results.')
        self.assertEquals(target['first'], 'value1', 
            'Multiple key-value pairs are not working. Expected "first" = "value1".')
        self.assertEquals(target['second'], 'value2', 
            'Multiple key-value pairs are not working. Expected "second" = "value2".')
        
        # Test that empty lines are ignored.
        target = Config._Parse('\n\na=1\n\n\nb=2\n\n')
        self.assertEquals(len(target), 2, 'Empty lines are not being ignored. Expected 2 results.')
        self.assertEquals(target['a'], '1', 'Empty lines are not being ignored. Expected a = 1.')
        self.assertEquals(target['b'], '2', 'Empty lines are not being ignored. Expected b = 2.')
    
        # Test full line commenting.
        target = Config._Parse('#commented\na=2')
        self.assertEquals(len(target), 1, 'Full line comments not being ignored. Expected 1 result.')
        self.assertEquals(target['a'], '2', 'Full line comments not being ignored. Expected a = 2.')
        

if __name__ == "__main__":
    unittest.main()
    
    
    
    
    
    
    
    
    
    
    
