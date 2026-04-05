# test_problem1.py
import unittest
from problem1 import *

class TestProblem1(unittest.TestCase):

    def test_problem1_init(self):
        word = "HelloWorld"
        subset = SubSets(word)
        self.assertEqual("SubSets(HelloWorld)", subset.__repr__())

    def test_all_substrings(self):
        word = "1234"
        result = SubSets(word)

        self.assertEqual(list(result), ['1', '12', '123', '1234', '2', '23', '234', '3', '34', '4'])


if __name__ == '__main__':
    unittest.main()