# problem3.py

def sequential_search(collection, key) -> bool:

    if len(collection) == 0:
        return False
    if collection[0] == key:
        return True
    else: return sequential_search(collection[1:], key)

# Takes O(n⋀2) n squared time
# Takes O(n) memory
# It could reduce memory

def binary_search(collection, key) -> bool:

    if len(collection) == 0:
        return False

    middle = collection[len(collection) // 2]
    if key < middle:
        return binary_search(collection[:len(collection) // 2], key)
    elif key > middle:
        return binary_search(collection[len(collection) // 2:], key)
    elif key == middle:
        return True

# Takes O(nlog(n)) time
# Takes O(n) memory
# It can reduce the amount of memory needed.