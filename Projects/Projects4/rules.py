# rules.py

from collections import namedtuple
import random


Option = namedtuple("Option", ["probability", "content"])

class Rule:

    def __init__(self, name: str, options: list[str]):
        self._name = name.strip("\n")
        self._options = list()
        self._total_events = 0
        self._set_options(options)

    def total_events(self) -> int:
        """Returns the total number of events this rule has."""
        return self._total_events

    def _set_options(self, options: list[str]):
        """It iterates through the lines and assigns probability accordingly"""
        for option in options:
            words = option.strip("\n").split()
            self._options.append(Option((self._total_events, int(words[0]) + self._total_events), option[len(words[0])+1:]))
            self._total_events += int(words[0])

    def get_option(self) -> Option.content:
        """@returns the contents of the options in the rule based on its
        probability"""
        random_index = random.randint(0, self._total_events-1)
        for option in self._options:
            if option.probability[0] <= random_index <= option.probability[1]:
                return option.content

    def name(self) -> str:
        """@return name of the rule"""
        return self._name

class Grammar:
    def __init__(self, rules: list[Rule]):
        self._rules = dict()
        self._set_rules(rules)

    def _set_rules(self, rules: list[Rule]):
        """It sets a dictionary of rules"""
        for rule in rules:
            self._rules[rule.name()] = rule

    def evaluate_rule(self, rule: Rule) -> str:
        """@returns the evaluated value of the rule"""
        words = rule.get_option().split()
        value = ""
        for word in words:
            if word.startswith("[") and word.endswith("]"):
                value += " " + self.evaluate_rule(self.rule(word[1:-1]))
            else: value += " " + word
        return value.strip()

    def rule(self, key: str) -> Rule:
        """@return a rule based on key"""
        return self._rules[key]