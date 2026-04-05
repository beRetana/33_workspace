# test_problem3.py

import unittest
from problem3 import *

class Test(unittest.TestCase):
    def test_creation(self):
        base = Base(3,4)
        self.assertEqual(base.get_value_one(), 3)
        self.assertEqual(base.get_value_two(), 4)

    def test_equality(self):
        base1 = Base(3,4)
        base2 = Base(3,4)
        base3 = Base("3",4)
        self.assertEqual(base1, base2)
        self.assertNotEqual(base1, base3)

    def test_derived_class_has_same_methods(self):
        derived1 = Derived(1,2,3)
        derived2 = Derived(1,2,3)
        derived3 = Derived(1, "two", 3)
        self.assertEqual(derived1.get_value_one(), 1)
        self.assertEqual(derived1.get_value_two(), 2)
        self.assertEqual(derived1.get_value_three(), 3)
        self.assertEqual(derived1, derived2)
        self.assertNotEqual(derived1, derived3)

    def test_derived_class_not_equal_to_base(self):
        base1 = Base(1,2)
        derived1 = Derived(1,2,3)
        self.assertNotEqual(base1, derived1)
        self.assertNotEqual(derived1, base1)
        base1 = Base("45", 2)
        derived1 = Derived("45", 2, True)
        self.assertNotEqual(base1, derived1)
        self.assertNotEqual(derived1, base1)

if __name__ == "__main__":
    unittest.main()
