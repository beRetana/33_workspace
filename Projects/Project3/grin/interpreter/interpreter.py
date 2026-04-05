# interpreter.py

from grin.interpreter import commads

class Interpreter:

    def __init__(self):
        self._variables_stack = dict()
        self._labels_stack = dict()
        self._gosub_stack = list()

    def variable_stack(self) -> dict:
        """@return The stack of variables in memory"""
        return self._variables_stack

    def labels_stack(self) -> dict:
        """@return The stack of labels in memory"""
        return self._labels_stack

    def gosub_stack(self) -> list:
        """@return The stack of gosubs in memory"""
        return self._gosub_stack

    def add_gosub(self, line_index: int):
        """Stores the location of the GOSUB"""
        self._gosub_stack.append(line_index)

    def add_label(self, label: str, line_number: int):
        """Adds a label to the stack"""
        self._labels_stack[label] = line_number

    def get_label(self, label: str) -> int:
        """If found, returns the line number of the label"""
        if label in self._labels_stack: return self._labels_stack[label]

    def get_variable(self, name) -> int|str|float|None:
        """If found, it returns the value of the variable."""
        if name in self._variables_stack: return self._variables_stack[name]

    def add_variable(self, variable: commads.Identifier) -> None:
        """Adds a variable to the stack or overrides its value if already present."""
        self._variables_stack[variable.first_argument()] = variable.value()

    @staticmethod
    def print(value: commads.Print) -> None:
        value.print_value()

