# test_problem2.py

import unittest
from problem2 import *

class Test(unittest.TestCase):
    def test_equivalence(self):
        self.assertEqual(Collection((1,2,3,4)), (Collection([1,2,3,4])))
        self.assertEqual(Collection("Hello World"), Collection('Hello World'))
        self.assertNotEqual(Collection([1,2,3,4]), Collection([1,2,4]))
        self.assertNotEqual(Collection([1, 2, 3, 4]), Collection([1, 2, 4, 3]))
        self.assertNotEqual(Collection("HelloWorld"), Collection('Hello World'))
        self.assertNotEqual(Collection("HelloWorld"), "HelloWorld")
        self.assertNotEqual(Collection([1,2,3,4]), [1,2,3,4])

    def test_less_or_equal(self):
        self.assertLessEqual(Collection([1,2,3,4]), Collection([1,2,3,5]))
        self.assertLessEqual(Collection((1, 2, 3)), Collection([1, 2, 3, 5]))
        self.assertLessEqual(Collection("Hello"), Collection("HelloWorld"))

    def test_greater_than(self):
        self.assertGreater(Collection([1,2,3,7,8]), Collection([0,1,2,5]))
        self.assertGreater(Collection((1, 2, 3, 4)), Collection([0, 1, 2]))
        self.assertGreater(Collection([5, 6]), Collection([1, 2]))
        self.assertGreater(Collection("1234"), Collection("012"))
        self.assertGreater(Collection([1, 2, 3]), Collection([0, 1]))
        self.assertGreater(Collection('cba'), Collection('aa'))

    def test_less_than(self):
        self.assertLess(Collection([1, 2, 3]), Collection([4, 5, 6]))
        self.assertLess(Collection([2, 3]), Collection([3, 4]))
        self.assertLess(Collection([1, 1]), Collection([2, 2]))
        self.assertLess(Collection(["bat", "dog"]), Collection(["cat", "doggy"]))
        self.assertLess(Collection(["apple", "banana"]), Collection(["banana", "cherry"]))

    def test_greater_than_or_equal(self):
        self.assertGreaterEqual(Collection([5, 6, 7]), Collection([1, 2, 3]))
        self.assertGreaterEqual(Collection([3, 2]), Collection([1, 2]))
        self.assertGreaterEqual(Collection([5, 4]), Collection([5, 3]))


if __name__ == '__main__':
    unittest.main()