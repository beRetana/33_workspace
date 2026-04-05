# test_commands.py
import contextlib
import unittest
from contextlib import redirect_stdout
from io import StringIO
from grin.interpreter.commads import *

class TestCommands(unittest.TestCase):

    def test_general_class(self):
        general = Command("First Command")

        self.assertEqual(general.first_argument(), "First Command")

    def test_general_subclass(self):
        variable = Identifier("X", 23)
        self.assertEqual(variable.first_argument(), "X")
        self.assertEqual(variable.value(), 23)

    def test_printing(self):
        printer = Print("Hello World!")
        with contextlib.redirect_stdout(StringIO()) as output:
            printer.print_value()
        self.assertEqual(output.getvalue().strip(), "Hello World!")

if __name__ == '__main__':
    unittest.main()