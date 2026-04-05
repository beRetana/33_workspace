# test_input_processor.py

import unittest
from contextlib import redirect_stdout
from io import StringIO

from grin.interpreter import input_processor

class TestInputProcessor(unittest.TestCase):

    def setUp(self):
        self._processor = input_processor.InputProcessor()

    def send_input(self, pseudo_inputs):
        with redirect_stdout(StringIO()) as outcome:
            self._processor.send_input(pseudo_inputs)
        return outcome.getvalue()

    def test_sending_input_with_non_existent_variables(self):
        pseudo_inputs = ['LET NAME NO']
        outcome = self.send_input(pseudo_inputs)
        self.assertFalse(True if outcome == "Variable NO does not exist" else False)

    def test_sending_input_with_valid_variables(self):
        pseudo_inputs = ['LET NAME "Boo"', 'LET NAME "Boo"','LET AGE 13.015625', 'LET AGE NAME', 'LET DAYS 23']
        outcome = self.send_input(pseudo_inputs)
        expected = {'NAME': 'Boo', 'AGE': 'Boo', 'DAYS': 23}
        self.assertEqual(expected, self._processor.interpreter().variable_stack())
        self.assertTrue(True if outcome == "" else False)

    def test_sending_input_with_valid_prints(self):
        pseudo_inputs = ['LET NAME "Hello World1"', 'PRINT NAME', 'PRINT "Hello World2"']
        outcome = self.send_input(pseudo_inputs).split('\n')
        self.assertTrue(True if outcome[0].strip() == "Hello World1" else False)
        self.assertTrue(True if outcome[1].strip() == "Hello World2" else False)

    def test_sending_input_with_empty_variable(self):
        pseudo_inputs = ['LET NAME A']
        outcome = self.send_input(pseudo_inputs).strip()
        self.assertTrue(True if outcome == "" else False)

    def test_sending_input_for_adding_to_a_valid_variable(self):
        pseudo_inputs = ['LET I 3', 'LET B 15.5', 'ADD I 2', 'ADD I B',
                         'LET A "HELLO"', 'LET C "WORLD!"', 'LET B " "', 'ADD A B', 'ADD A C']
        self._processor.send_input(pseudo_inputs)
        expected = {'I': 20.5, 'B': ' ', 'A': 'HELLO WORLD!', 'C': 'WORLD!'}
        self.assertEqual(expected, self._processor.interpreter().variable_stack())

    def test_sending_input_for_adding_to_invalid_variable(self):
        pseudo_inputs = ['LET A 3', 'LET B "5"', 'ADD A B']
        outcome = self.send_input(pseudo_inputs).strip()
        self.assertTrue(True if outcome == "Type Error: 3, and 5" else False)

    def test_sending_input_for_subtracting_to_a_valid_variable(self):
        pseudo_inputs = ['LET I 3', 'LET B 15.5', 'SUB I 2', 'SUB I B']
        self._processor.send_input(pseudo_inputs)
        expected = {'I': -14.5, 'B': 15.5}
        self.assertEqual(expected, self._processor.interpreter().variable_stack())

    def test_sending_input_for_subtracting_to_invalid_variable(self):
        pseudo_inputs = ['LET A 3', 'LET B "5"', 'SUB A B']
        outcome = self.send_input(pseudo_inputs).strip()
        self.assertTrue(True if outcome == "Type Error: 3, and 5" else False)

    def test_sending_input_for_dividing_to_a_valid_variable(self):
        pseudo_inputs = ['LET A 20', 'LET B 4.0', 'DIV A 2', 'DIV A B']
        self._processor.send_input(pseudo_inputs)
        expected = {'A': 2.5, 'B': 4.0}
        self.assertEqual(expected, self._processor.interpreter().variable_stack())

    def test_sending_input_for_dividing_to_invalid_variable(self):
        pseudo_inputs = ['LET A 20', 'LET B "4"', 'DIV A B']
        outcome = self.send_input(pseudo_inputs).strip()
        self.assertTrue(True if outcome == "Type Error: 20, and 4" else False)

    def test_sending_input_for_dividing_by_zero(self):
        pseudo_inputs = ['LET A 20', 'DIV A 0']
        outcome = self.send_input(pseudo_inputs).strip()
        self.assertTrue(True if outcome == "Arithmetic Error for 20/0" else False)

    def test_sending_input_for_flags(self):
        pseudo_inputs = ['FLAG: LET A 20']
        outcome = self.send_input(pseudo_inputs).strip()
        self.assertTrue(True if outcome == "" else False)

    def test_sanity_check(self):
        pseudo_inputs = ['LET MESSAGE "Hello Boo!"', 'PRINT MESSAGE', '.']
        outcome = self.send_input(pseudo_inputs).strip()
        self.assertTrue(True if outcome == "Hello Boo!" else False)

    def test_multiplication(self):
        pseudo_inputs = [
            'LET A 4',
            'MULT A 2',
            'PRINT A',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["8"]
        expected_variables = {'A': 8}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_mult_with_strings(self):
        pseudo_inputs = [
            'LET A "Hello"',  # Assign "Hello" to A
            'LET B 3',  # Assign 3 to B
            'MULT A B',  # Multiply A by B (A = "Hello" * 3 = "HelloHelloHello")
            'PRINT A',  # Print the value of A ("HelloHelloHello")
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["HelloHelloHello"]  # Expected printed output
        expected_variables = {'A': "HelloHelloHello", 'B': 3}  # Final values of A and B
        expected_labels = {}  # No labels used

        # Assertions to check the outcomes
        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_write_up_labels(self):
        pseudo_inputs = ['LET A 3', 'PRINT A', 'GOSUB "CHUNK"',
                         'PRINT A', 'PRINT B', 'GOTO "FINAL"',
                         'CHUNK:  LET A 4', 'LET B 6', 'RETURN',
                         'FINAL:  PRINT A', '.']
        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["3", "4", "6", "4"]
        expected_variables = {'A': 4, 'B': 6}
        expected_labels = {'CHUNK':6, 'FINAL':9}
        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_some_very_complicated_tests(self):
        pseudo_inputs = [
            'LET A 6',  # A=6
            'LET B 3',  # B=3
            'MULT A 2',  # A=12
            'PRINT A',  # 12
            'GOSUB "CHUNK"',  # Go to CHUNK
            'PRINT A',  # 36
            'DIV B 2',  # B=2
            'PRINT B',  # 2
            'GOTO "FINAL"',  # Go to FINAL
            'CHUNK:  MULT A 3',  # A = 36
            'LET B 4',  # B = 4
            'RETURN',  # Return
            'FINAL:  PRINT A',  # 36
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["12", "36", "2", "36"]
        expected_variables = {'A': 36, 'B': 2}
        expected_labels = {'CHUNK': 9, 'FINAL': 12}  # Line numbers for CHUNK and FINAL labels

        # Assertions to check the outcomes
        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_variables_from_write_up(self):
        pseudo_inputs = [
            'LET NAME "Boo"',
            'LET AGE 13.015625',
            'PRINT NAME',
            'PRINT AGE',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["Boo", "13.015625"]
        expected_variables = {'NAME': "Boo", 'AGE': 13.015625}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_flow(self):
        pseudo_inputs = [
            'LET A 1',
            'GOTO 2',
            'LET A 2',
            'PRINT A',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["1"]
        expected_variables = {'A': 1}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_arithmetics(self):
        pseudo_inputs = [
            'LET A 4', # A = 4
            'ADD A 3', # A = 7
            'PRINT A', # 7
            'LET B 5', # B = 5
            'SUB B 3', # B = 2
            'PRINT B', # 2
            'LET C 6', # C = 6
            'MULT C B',# C = 12
            'PRINT C', # 12
            'LET D 8', # D = 8
            'DIV D 2', # D = 4
            'PRINT D', # 4
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()

        expected_printed = ["7", "2", "12", "4"]
        expected_variables = {'A': 7, 'B': 2, 'C': 12, 'D': 4}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_gosub_from_write_up(self):
        pseudo_inputs = [
            'LET A 1',
            'GOSUB 4',
            'PRINT A',
            'PRINT B',
            'END',
            'LET A 2',
            'LET B 3',
            'RETURN',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()

        expected_printed = ["2", "3"]
        expected_variables = {'A': 2, 'B': 3}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_subgo_with_labels(self):
        pseudo_inputs = [
            'LET A 2',
            'GOSUB "PRINTABC"',
            'LET B 2',
            'GOSUB "PRINTABC"',
            'LET C 3',
            'GOSUB "PRINTABC"',
            'LET A 1',
            'GOSUB "PRINTABC"',
            'END',
  'PRINTABC: PRINT A',
            'PRINT B',
            'PRINT C',
            'RETURN',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()

        expected_printed = ["2", "0", "0", "2", "2", "0", "2", "2", "3", "1", "2", "3"]
        expected_variables = {'A': 1, 'B': 2, 'C': 3}
        expected_labels = {"PRINTABC": 9}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_more_subgo_nested(self):
        pseudo_inputs = [
            'LET A 1',
            'GOSUB 5',
            'PRINT A',
            'END',
            'LET A 3',
            'RETURN',
            'PRINT A',
            'LET A 2',
            'GOSUB -4',
            'PRINT A',
            'RETURN',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["1", "3", "3"]
        expected_variables = {'A': 3}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_goto_conditionals(self):
        pseudo_inputs = [
            'LET A 3',
            'LET B 5',
            'GOTO 2 IF A < 4',
            'PRINT A',
            'PRINT B',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).split()
        expected_printed = ["5"]
        expected_variables = {'A': 3, 'B': 5}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_greater_than(self):
        pseudo_inputs = [
            'LET A 7',
            'LET B 5',
            'GOTO 1 IF A > B',
            'PRINT "A is greater than B"',
            'END',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).strip()

        expected_printed = "A is greater than B"
        expected_variables = {'A': 7, 'B': 5}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

    def test_greater_than_equal(self):
        pseudo_inputs = [
            'LET A 7',
            'LET B 7',
            'GOTO 1 IF A >= B',
            'PRINT "A is greater than or equal B"',
            'END',
            '.'
        ]

        outcome = self.send_input(pseudo_inputs).strip()

        expected_printed = "A is greater than or equal B"
        expected_variables = {'A': 7, 'B': 7}
        expected_labels = {}

        self.assertEqual(expected_printed, outcome)
        self.assertEqual(expected_variables, self._processor.interpreter().variable_stack())
        self.assertEqual(expected_labels, self._processor.interpreter().labels_stack())

if __name__ == '__main__':
    unittest.main()




