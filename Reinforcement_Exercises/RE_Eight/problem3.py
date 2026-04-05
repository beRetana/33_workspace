# problem3.py

class LimitedString:

    _id = -1

    def __init__(self, limit, can_delete = True):
        if type(limit) != int or (0 > limit): raise ValueError
        self._limit = limit
        self._can_delete = can_delete
        self._id = LimitedString._id + 1

    @property
    def name(self):
        return str(self._id)

    def __set__(self, obj, value):
        if type(value) != str or ( len(value) > self._limit): raise ValueError
        obj.__dict__[self.name] = value

    def __get__(self, obj, tipo):
        try: return obj.__dict__[self.name]
        except KeyError: raise AttributeError

    def __delete__(self, obj):
        if not self._can_delete: raise AttributeError
        try: del obj.__dict__[self.name]
        except KeyError: raise AttributeError