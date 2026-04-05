# problem2.py

class Collection:
    def __init__(self, values):
        self._values = values

    def get_values(self):
        return self._values

    def __eq__(self, other):
        return self.iterate_values( self, other, lambda first, second: first != second, False)

    def __le__(self, other):
        return self.iterate_values(self, other, lambda first, second: first > second,True)

    def __lt__(self, other):
        return self.iterate_values(self, other, lambda first, second: first >= second,True)

    @staticmethod
    def iterate_values(first: 'Collection', second: 'Collection', inequality, second_bigger):
        if not isinstance(second, type(first)): return False
        second_iter = iter(second.get_values())

        for value in first.get_values():
            try:
                if inequality(value, next(second_iter)): return False
            except StopIteration: return False
        try:
            next(second_iter)
        except StopIteration: return True
        else: return second_bigger