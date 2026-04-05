#problem2.py
from decimal import FloatOperation
from itertools import combinations


def generator_range(stop:int, start=None, step=None, /)->iter:

    if step == 0:
        raise ValueError('step cannot be zero')

    if start is None and step is None:
        start = 0
        step = 1
    elif start is not None and step is None:
        start, stop = stop, start
        step = 1
    else:
        start, stop = stop, start

    index = 0

    while index < (stop-start)/step:
        yield start + (index * step)
        index += 1

def no_fizz_without_buzz(start:int)-> iter:

    index = 0

    while True:
        value = start + index
        if value % 15 == 0:
            yield value
            index += 1
        elif value % 3 == 0 or value % 5 == 0:
            index += 1
            continue
        else:
            yield value
            index += 1


def cartesian_product(*kwargs)->list:

    if len(kwargs) == 0:
        return []

    indexes_max = []
    indexes = []
    permutations = 1

    for kwarg in kwargs:
        indexes_max.append(len(kwarg))
        permutations *= len(kwarg)
        indexes.append(0)

    for permutation in range(permutations):

        value = []
        for iterable_index in range(len(kwargs)):
            value.append(kwargs[iterable_index][indexes[iterable_index]])

        yield tuple(value)

        indexes[0] += 1
        for index in range(len(indexes_max)-1):
            if indexes[index] == indexes_max[index]:
                indexes[index] = 0
                indexes[index+1] += 1







