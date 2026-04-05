# problem1.py

class SubSets:

    def __init__(self, word: str):
        self._word = word
        self._word_index = 0
        self._substring_index = 0

    def __iter__(self):
        return SubSets(self._word)

    def __next__(self)-> str:
        if self._word_index >= len(self._word)-1:
            raise StopIteration
        if self._substring_index >= len(self._word):
            self._word_index += 1
            self._substring_index = self._word_index + 1
        else:
            self._substring_index += 1

        return self._word[self._word_index: self._substring_index]

    def __repr__(self):
        return f'SubSets({self._word})'


def all_substrings(word):
    """Returns a set of all possible subsets of the given word"""
    return SubSets(word)