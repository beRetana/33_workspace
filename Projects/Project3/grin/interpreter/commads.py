# commands.py
from grin import GrinToken

class Command:

    def __init__(self, first_argument):
        self._first_argument = first_argument

    def first_argument(self) -> str|int|float:
        return self._first_argument

class Identifier(Command):

    def __init__(self, name, value = 0):
        super().__init__(name)
        self._value = value

    def update(self, new_value) -> None:
        self._value = new_value

    def value(self)-> int|float|str:
        return self._value

class Print(Command):

    def __init__(self, first_argument):
        super().__init__(first_argument)

    def print_value(self):
        print(self.first_argument())

class Comparison(Command):
    def __init__(self, first_argument: GrinToken, second_argument: GrinToken):
        super().__init__(first_argument)
        self._second_argument = second_argument

    def second_argument(self) -> GrinToken:
        return self._second_argument

    def evaluate(self, expression) -> bool:
        try:
            value = expression(self.first_argument(), self.second_argument())
        except TypeError as e:
            print(e)
            return False
        else:
            return value

