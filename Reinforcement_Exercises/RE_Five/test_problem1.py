# test_problem1.py
import unittest
from problem1 import *

class TestProblem1(unittest.TestCase):
    def test_problem_check_len_new_object(self):
        self.assertEqual(0, len(MultipleSequence(0)))

    def test_problem_check_truthy_value(self):
        self.assertTrue(MultipleSequence(1))
        self.assertFalse(MultipleSequence(0))

    def test_next_item_returned(self):
        sequence = MultipleSequence(10, 5)
        next(sequence)
        next_value = 5
        self.assertEqual(next_value, next(sequence))

    def test_iter_sequence(self):
        size = 10
        sequence = MultipleSequence(size, 5)
        counter = 0
        for value in sequence:
            counter += 1

        self.assertEqual(size, counter)

        sequence_list = MultipleSequence(size, 3)
        expected = [0,3,6,9,12,15,18,21,24,27]

        self.assertEqual(expected, list(sequence_list))

    def test_indexing(self):
        size = 10
        sequence = MultipleSequence(size, 5)

        for index in range(len(sequence)):
            self.assertEqual(index*5, sequence[index])

    def test_negative_indexing(self):
        size = 10
        sequence = MultipleSequence(size, 5)
        for index in range(1, len(sequence)):
            self.assertEqual(50-(5*index), sequence[-index])

    def test_check_in_value(self):
        sequence = MultipleSequence(10, 5)
        self.assertIn(25, sequence)
        self.assertIn(0, sequence)
        self.assertNotIn(27, sequence)
        self.assertNotIn(50, sequence)
        self.assertNotIn(-5, sequence)
        self.assertNotIn(-3, sequence)

    def test_representation(self):
        size = 10
        self.assertEqual("MultipleSequence(10, 5)", str(MultipleSequence(size, 5) ))
        self.assertEqual("MultipleSequence(10)", str(MultipleSequence(size, 1) ))
        self.assertEqual("MultipleSequence(10)", str(MultipleSequence(size)))

if __name__ == '__main__':
    unittest.main()