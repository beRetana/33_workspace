# project4.py
#
# ICS 33 Winter 2025
# Project 4: Still Looking for Something
from operator import contains
from pathlib import Path
from rules import Rule, Grammar

def create_grammar(sections: list[list[str]]) -> Grammar:
    rules = []
    for section in sections:
        rules.append(Rule(section[0], section[1:]))

    return Grammar(rules)

def search_rules(lines: list[str]) -> [list[str]]:
    """@returns a list of lines for a rule"""
    start_index = 0
    line_index = 0
    for line in lines:
        if line.__contains__("{"):
            start_index = line_index + 1
        elif line.__contains__("}"):
            yield lines[start_index:line_index]
        line_index += 1

def read_file(path: Path) -> list[list[str]]:
    """@returns a list with a set of lines that contain the rules"""

    with path.open('r') as file:
        return list(search_rules(file.readlines()))

def main() -> None:
    path = input()

    rule_lines = read_file(Path(path))
    grammar = create_grammar(rule_lines)

    number_of_eval = int(input())
    rule_name = input()

    for _ in range(number_of_eval):
        print(grammar.evaluate_rule(grammar.rule(rule_name)))

if __name__ == '__main__':
    main()
