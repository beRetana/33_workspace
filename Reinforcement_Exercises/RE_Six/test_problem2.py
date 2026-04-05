# test_problem2.py

import unittest
from problem2 import *

class Test(unittest.TestCase):

    def test_sales_booking(self):
        tag = "Donuts"
        sales_list = [3.56, 342, 65, 3.56, 4.5, 1.2, 7.8, 10]
        year = 2025

        booking = SalesBooking(tag, sales_list, year)

        self.assertEqual(booking.__hash__(), hash((tag, year)))

    def test_dev_tracker(self):
        tag = "Super Mario Bross"
        tasks_list = [3.56, "Interaction", 65, "Movement", 4.5, "Animations", 7.8, 10]
        size = 500
        budget = 500
        manager = "Marisol"

        dev_project = DevelopmentTracker(tag, tasks_list, size, budget, manager)

        self.assertEqual(dev_project.__hash__(), hash(( size, manager, budget, tag )))

if __name__ == "__main__":
    unittest.main()