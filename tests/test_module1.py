# tests/test_module1.py

import unittest
from greydata import module1

class TestModule1(unittest.TestCase):
    
    def test_hello(self):
        self.assertEqual(module1.hello(), "Hello from greydata!")
    
    def test_add_numbers(self):
        self.assertEqual(module1.add_numbers(1, 2), 3)
        self.assertEqual(module1.add_numbers(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
