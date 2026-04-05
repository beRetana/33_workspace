# problem2.py

def multiplies(count: int, multiplier: int) -> list[int]:

    return [x*multiplier for x in range(1, count+1)]

def with_non_zero_lengths(*args) -> dict['argument', int]:

    return {key : len(key) for key in args if len(key) != 0 }

def make_diagonal(n:int)-> list[list[None|str]]:

    return [[None if column != row else "B" for column in range(n)] for row in range(n)]

"""
if __name__ == "__main__":
   print(with_non_zero_lengths("Boo", "is", "Happy"))
   print(with_non_zero_lengths(range(3), range(0), range(1)))
   print(make_diagonal(3))
   print(make_diagonal(1))
   print(make_diagonal(2))
"""
