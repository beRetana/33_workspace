# problem3.py

import random

def cached(size):
    def decorator(function):
        cache = {}
        def wrapper(*args, **kwargs):
            if not (_is_hashable(args) or _is_hashable(kwargs)): return function(*args, **kwargs)
            key = (tuple(args), tuple(kwargs))
            if _is_in_cache(cache, key): return cache[key]
            if 0 <= len(cache) < size: cache[key] = function(*args, **kwargs)
            else:
                random_index = random.randint(0, len(cache) - 1)
                index = 0
                for cache_key in cache.keys():
                    if index == random_index:
                        del cache[cache_key]
                        break
                    index += 1
                cache[key] = function(*args, **kwargs)
            return cache[key]
        return wrapper
    return decorator

def _is_in_cache(cache:dict, keys:tuple):
    if len(cache) == 0: return False
    for key in cache.keys():
        if list(keys[0]) == list(key[0]) and set(keys[1]) == set(key[1]): return True
    return False

def _is_hashable(iterable):
    for item in iterable:
        try:
            hash(item)
            return True
        except NotImplementedError or TypeError:
            return False