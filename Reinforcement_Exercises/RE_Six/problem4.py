# problem4.py

def make_repeater(repeatable_function, repeat_count):
    def repeater(value):
        for _ in range(repeat_count):
            value = repeatable_function(value)
        return value
    return repeater


