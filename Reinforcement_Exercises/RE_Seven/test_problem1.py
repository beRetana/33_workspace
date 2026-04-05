import unittest
from functools import partial

from problem1 import *

class Test(unittest.TestCase):

    def test_normal_multiply_with_one_argument(self):
        def multiply(x, y):
            return x * y

        multiply_by_3 = partial(multiply, 3)
        multiply_by_5 = partial(multiply, 5)
        multiply_by_0 = partial(multiply, 0)
        multiply_by_negative_57 = partial(multiply, -57)

        self.assertEqual(multiply_by_3(2), 6)
        self.assertEqual(multiply_by_5(2), 10)
        self.assertEqual(multiply_by_0(1034), 0)
        self.assertEqual(multiply_by_negative_57(-41), 2337)

    def test_multiply_with_one_positional_argument(self):
        def multiply(x, y):
            return x * y
        multiply_by_3 = partial(multiply, x = 3)
        multiply_by_5 = partial(multiply, y = 5)

        self.assertEqual(multiply_by_3(y = 2), 6)
        self.assertEqual(multiply_by_5(x = 2), 10)
        self.assertEqual(multiply_by_5(10), 50)

    def test_multiply_with_two_positional_argument(self):
        def multiply(x, y):
            return x * y
        multiply_by_3 = partial(multiply, x = 3, y = 3)
        multiply_by_5 = partial(multiply, x = 5, y = 5)
        self.assertEqual(multiply_by_3(), 9)
        self.assertEqual(multiply_by_5(), 25)

    def test_multiply_with_no_positional_arguments(self):
        def multiply(x, y):
            return x * y
        three_squared = partial(multiply, 3, 3)
        five_squared = partial(multiply, 5, 5)

        self.assertEqual(three_squared(), 9)
        self.assertEqual(five_squared(), 25)

    def test_invalid_multiply(self):
        def multiply(x, y):
            return x * y

        invalid_multiply = partially_call(multiply, q = 5)
        invalid_multiply_two = partial(multiply, x = 5)

        with self.assertRaises(TypeError):invalid_multiply(x=2)
        with self.assertRaises(TypeError):invalid_multiply_two(5)
        with self.assertRaises(TypeError):invalid_multiply_two(5, 3)
        with self.assertRaises(TypeError):invalid_multiply_two(5, y = 3)

if __name__ == '__main__':
    unittest.main()
