# problem1.py

class MultipleSequence:

    def __init__(self, length, multiplier = 1, /):
        self._length = length
        self._multiplier = multiplier
        self._index = 0

    def __bool__(self):
        if len(self): return True
        return False

    def __len__(self):
        return self._length

    def __next__(self):
        if self._index >= len(self): raise StopIteration
        self._index += 1
        return self._get_index_value(self._index-1)

    def __getitem__(self, index):
        if -len(self) >= index >= len(self): raise IndexError
        return self._get_index_value(index)

    def _get_index_value(self, index = 0):
        if index < 0:
            return self._multiplier * (self._length + index)
        return self._multiplier * index

    def __contains__(self, item):
        if item % self._multiplier == 0:
            return  -1 < item / self._multiplier < len(self)
        return False

    def __iter__(self):
        return MultipleSequence(self._length, self._multiplier)

    def __repr__(self):
        multiplier = ""
        if self._multiplier != 1:
            multiplier = f", {self._multiplier}"
        return f'{self.__class__.__name__}({self._length}{multiplier})'
