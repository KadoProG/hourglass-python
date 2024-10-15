def find_index(iterable, condition) -> int:
    for i, item in enumerate(iterable):
        if condition(item):
            return i
    return -1
