# test_problem2.py

import unittest
from problem2 import *

class TestProblem2(unittest.TestCase):

    def test_problem2_generate_range(self):
        self.assertEqual(list(generator_range(5)), list(range(5)))
        self.assertEqual(list(generator_range(2, 10)), list(range(2, 10)))
        self.assertEqual(list(range(2, 10,3)), list(generator_range(2, 10, 3)))
        self.assertEqual(list(generator_range(30,2)), list(range(30,2)))
        self.assertEqual(list(generator_range(11, 1, 2)), list(range(11, 1, 2)))
        self.assertEqual(list(generator_range(11, 1, -2)), list(range(11, 1, -2)))

    def test_problem2_infinite_sequence(self):

        def testing(start, n):
            sequence = no_fizz_without_buzz(start)

            return [next(sequence) for x in range(n)]

        self.assertEqual(testing(0,0), [])
        self.assertEqual(testing(1,0), [])
        self.assertEqual(testing(0,5), [0,1,2,4,7])

    def test_problem2_cartesian_product(self):

        self.assertEqual([], list(cartesian_product()))
        expected = [(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6)]
        self.assertEqual(expected, list(sorted(cartesian_product([1, 2, 3], [4, 5, 6]))))
        expected = [(1, 2), (1, 2), (1, 2), (1, 2)]
        self.assertEqual(expected, list(sorted(cartesian_product([1, 1], [2, 2]))))
        expected = [('B', 'C', 'D'), ('B', 'C', 'F'), ('B', 'D', 'D'), ('B', 'D', 'F'),
                    ('C', 'C', 'D'), ('C', 'C', 'F'), ('C', 'D', 'D'), ('C', 'D', 'F')]
        self.assertEqual(expected, list(sorted(cartesian_product('BC', 'CD', 'DF'))))

if __name__ == '__main__':
    unittest.main()