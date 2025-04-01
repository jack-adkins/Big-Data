import operator
from functools import reduce

def add(*arguments):
    return reduce(operator.add, arguments)

def sub(*arguments):
    return reduce(operator.sub, arguments)

def ra_sub(*arguments):
    arguments = reversed(arguments)
    return reduce(lambda x, y: operator.sub(y, x), arguments)

# Example usage:
print(add(1, 2, 3))   # Output: 6
print(sub(5, 1, 2))   # Output: 2
print(ra_sub(5, 1, 2))  # Output: 6
