# test_problem3.py

import unittest
from problem3 import *

class Test(unittest.TestCase):

    def test_call(self):
        class Cosa:
            variable = LimitedString(10, False)
        cosa = Cosa()
        cosa.variable = "Hola Mundo"
        print(cosa.variable)
        del cosa.variable

if __name__ == '__main__':
    unittest.main()