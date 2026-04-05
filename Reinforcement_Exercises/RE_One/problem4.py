# problem4.py

import contextlib
from contextlib import nullcontext
from logging import exception


class DifferentErrorTypes(Exception):

    def __init__(self, expected: Exception, actual: Exception | str) -> None:
        """Initializes the exception, given an expected and actual Exception."""
        self._expected = expected
        self._actual = actual

    def __str__(self) -> str:
        return f'The exception type raised {self._actual} does not match the expected type {self._expected}'

class MyContextManager:
    def __init__(self, error_type):
        self._error_type = error_type

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):

        if exc_type is None:
            raise DifferentErrorTypes(self._error_type.__name__, "None")
        if exc_type != self._error_type:
            raise DifferentErrorTypes(self._error_type.__name__, exc_type.__name__)
        return True


def shouldRaise(error_type):
    return MyContextManager(error_type)




