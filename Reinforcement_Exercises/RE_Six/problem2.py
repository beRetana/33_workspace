# problem2.py
from operator import contains


class HashableByAttributes:

    def __hash__(self):
        return hash(tuple(getattr(self, item) for item in dir(self) if "__" not in item and type(getattr(self, item)) in (int, float, str, bool)))

class SalesBooking(HashableByAttributes):
    def __init__(self, tag_name: str, sales_list: list[float], year: int):
        self._tag_name = tag_name
        self._sales_list = sales_list
        self._year = year

    def tag(self) -> str:
        return self._tag_name

    def sales(self) -> list[float]:
        return self._sales_list

    def year(self) -> int:
        return self._year


class DevelopmentTracker(HashableByAttributes):

    def __init__(self, tag_name: str, tasks_list: list[float], size: int, budget: float,
                 manager_name: str):
        self._tag_name = tag_name
        self._tasks_list = tasks_list
        self._size = size
        self._budget = budget
        self._manager_name = manager_name

    def tag(self):
        return self._tag_name

    def sales(self) -> list[float]:
        return self._tasks_list

    def year(self) -> int:
        return self._size

    def manager_name(self) -> str:
        return self._manager_name

    def size(self) -> int:
        return self._size
