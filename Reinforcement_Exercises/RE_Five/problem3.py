# problem3.py

class Base:
    def __init__(self, value1, value2):
        self._value1 = value1
        self._value2 = value2

    def get_value_one(self):
        return self._value1

    def get_value_two(self):
        return self._value2

    def __eq__(self, other):
        if type(other) and not type(self) and issubclass(other.__class__, Base): return False
        return (self._value1 == other.get_value_one() and
                self._value2 == other.get_value_two())

class Derived(Base):
    def __init__(self, value1, value2, value3):
        super().__init__(value1, value2)
        self._value3 = value3

    def get_value_three(self):
        return self._value3

    def __eq__(self, other):
        try:
            return (self._value3 == other.get_value_three() and
                self._value1 == other.get_value_one() and
                self._value2 == other.get_value_two())
        except AttributeError:
            return False