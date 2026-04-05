# problem1.py

def class_method(func):
    def wrapper(cls, *args, **kwargs):
        func(cls, *args, **kwargs)
    return wrapper