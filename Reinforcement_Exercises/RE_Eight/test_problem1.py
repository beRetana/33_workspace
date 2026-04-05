# test_problem1.py

import unittest
from problem1 import *

class Test(unittest.TestCase):

    def test_decorator(self):

        class TestDecorator:

            count = 0

            def __init__(self):
                self.count += 1

            @classmethod
            def Count(cls):
                return cls.count

        TestDecorator.Count()
        TestDecorator().Count()


if __name__ == "__main__":
    unittest.main()