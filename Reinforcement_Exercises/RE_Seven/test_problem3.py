# test_problem3.py

import unittest

from problem3 import *



class Test(unittest.TestCase):

    def test_cache(self):
        @cached(5)
        def multiply(x, y):
            print(f"Function Executed: {x}*{y} = {x*y}")
            return x * y

        multiply(1, 1)
        print()
        multiply(1, 2)
        print()
        multiply(1, 3)
        print()
        multiply(1, 1)

        multiply(1, 4)
        print()
        multiply(1, 5)
        print()
        multiply(1, 6)
        print()
        multiply(1, 7)




if __name__ == '__main__':
    unittest.main()