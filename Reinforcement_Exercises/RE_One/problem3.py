# problem3.py
import io
import unittest
import contextlib
import printing

class TestPrinting(unittest.TestCase):

    def test_print_values_in_range_with_multiple_values(self):

        def tester(start_value, end_value, step_value):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                printing.print_values_in_range(start_value, end_value, step_value)

            output = output.getvalue()
            value = start_value
            for line in output.splitlines():
                self.assertEqual(str(value), line)
                value += step_value

        tester(0, 10, 1)
        tester(-5, 0, 1)
        tester(100, -100, -1)
        tester(10, 0, -2)

    def test_print_reversed_list_with_multiple_values(self):

        def tester(test_list: list):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                printing.print_reversed_list(test_list)

            output = output.getvalue()
            text_list = output.splitlines()
            for index in range(len(test_list)):
                test_value = test_list[index]
                test_value.reverse()
                self.assertEqual(str(test_value), str(text_list[index]))

        tester([[1,2], [2,3]])
        tester([["a", "b", "c"], [2, 3,4], [1.2, 5.4, 34], [True, False, True]])
        tester([])
        tester([["a", "b", "c", 2, True, -1.5, False, "Hello"]])
        tester([["a", "b"], ["c", 2, True], [-1.5, False, "Hello"]])