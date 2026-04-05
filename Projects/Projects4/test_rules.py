# test_rules.py

import unittest
from rules import *

class TestRules(unittest.TestCase):

    def test_create_one_rule(self):
        rule = Rule("Test", ["3 happy", "3 perfect", "1 relaxing", "1 fulfilled", "2 excited"])
        self.assertEqual(rule.name(), "Test")
        self.assertEqual(rule.total_events(), 10)
        for i in range(100):
            self.assertEqual(rule.get_option() in ["happy", "relaxing", "perfect", "fulfilled", "excited"], True)

        rule_1 = Rule("HowIsBoo", ["1 Boo is [Adjective] today"])
        self.assertEqual(rule_1.name(), "HowIsBoo")
        self.assertEqual(rule_1.total_events(), 1)
        for i in range(100):
            self.assertEqual(rule_1.get_option(), "Boo is [Adjective] today")

    def test_grammar_few_simple_rules(self):
        rule_1 = Rule("HowIsBoo", ["1 Boo is [Adjective] today"])
        rule_2 = Rule("Adjective", ["3 happy","3 perfect", "1 relaxing","1 fulfilled", "2 excited"])
        grammar = Grammar([rule_1, rule_2])
        self.assertEqual(grammar.rule("HowIsBoo"), rule_1)
        self.assertEqual(grammar.rule("Adjective"), rule_2)
        possible_answers = ["Boo is happy today", "Boo is perfect today", "Boo is relaxing today", "Boo is fulfilled today", "Boo is excited today"]
        for i in range(100):
            self.assertEqual(grammar.evaluate_rule(rule_1) in possible_answers, True)

if __name__ == '__main__':
    unittest.main()