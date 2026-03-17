from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map()
squared = list(map(lambda x: x ** 2, numbers))
print('Squared numbers:', squared)

# filter()
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print('Even numbers:', even_numbers)

# reduce()
product = reduce(lambda x, y: x * y, numbers)
print('Product of all numbers:', product)

# Other built-in functions
print('Length:', len(numbers))
print('Sum:', sum(numbers))
print('Minimum:', min(numbers))
print('Maximum:', max(numbers))
print('Sorted descending:', sorted(numbers, reverse=True))
