# test_project4.py

import unittest
from project4 import *

class TestProject4(unittest.TestCase):

    def setUp(self):
        self.boo_path = Path("/Users/brandon__lii/Downloads/UCI/2024-2025/Invierno/ICS_33/Projects/Projects4/boo_example.txt")
        self._boo_rule_lines = read_file(Path(self.boo_path))

    def test_lines_short_example(self):

        lines = ["{", "HowIsBoo", "1 Boo is [Adjective] today",
                "}", "", "{", "Adjective", "3 happy", "3 perfect", "1 relaxing", "1 fulfilled",
                "2 excited", "}"]

        result = list(search_rules(lines))

        expected = [["HowIsBoo", "1 Boo is [Adjective] today"], ["Adjective", "3 happy",
                    "3 perfect", "1 relaxing", "1 fulfilled", "2 excited"]]

        self.assertEqual(result, expected)

    def test_read_file_short_example(self):
        expected = [["HowIsBoo\n", "1 Boo is [Adjective] today\n"],
                    ["Adjective\n", "3 happy\n",
                     "3 perfect\n", "1 relaxing\n",
                     "1 fulfilled\n", "2 excited\n"]]

        self.assertEqual(self._boo_rule_lines, expected)

    def test_create_grammar(self):
        grammar = create_grammar(self._boo_rule_lines)
        possible_answers = ["Boo is happy today", "Boo is perfect today", "Boo is relaxing today",
                            "Boo is fulfilled today", "Boo is excited today"]
        for i in range(100):
            self.assertEqual(grammar.evaluate_rule(grammar.rule("HowIsBoo")) in possible_answers, True)

if __name__ == '__main__':
    unittest.main()