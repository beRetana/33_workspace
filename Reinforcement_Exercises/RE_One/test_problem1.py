# test_problem1.py
import unittest
import problem1

class TestProblem1(unittest.TestCase):
    def test_problem1_no_arguments(self):
        self.assertEqual(dict(),problem1.only_truthy())

    def test_problem1_with_keyword_arguments(self):
        self.assertEqual({'_name': 'Boo'}, problem1.only_truthy(name = "Boo"))
        expected = {'_b': 13, '_d': 'Boo'}
        self.assertEqual(expected, problem1.only_truthy( a = 0, b = 13, d = "Boo"))
        expected = {'_b': 13, '_d': 'Boo', '_name': 'Boo', '_true': True, '_true_double': 0.1,
                    '_non_empty_list': [0]}
        self.assertEqual(expected, problem1.only_truthy(a = 0, b = 13, d = "Boo", name = "Boo", true = True,
                                                        false = False, double = 0.0, true_double = 0.1,
                                                        empty_list = [], non_empty_list = [0]))

    def test_problem1_with_non_keyword_arguments(self):
        self.assertRaises(TypeError, problem1.only_truthy, 0, b = 13, d = "Boo")
        self.assertRaises(TypeError, problem1.only_truthy, '12', b = 13.5, d = "Boo")

if __name__ == '__main__':
    unittest.main()