# test_interpreter.py
import unittest
from unittest import TestCase
from grin.interpreter.interpreter import Interpreter
from grin.interpreter.commads import *

class TestInterpreter(TestCase):

    def setUp(self):
        self.interpreter = Interpreter()

    def test_interpreter_add_variables(self):
        variable = Identifier("NAME", "Brandon")
        self.interpreter.add_variable(variable)
        saved_variable = self.interpreter.get_variable("NAME")
        self.assertEqual(variable.value(), saved_variable)
        saved_variable = self.interpreter.get_variable("B")
        self.assertNotEqual(variable.value(), saved_variable)

if __name__ == "__main__":
    unittest.main()