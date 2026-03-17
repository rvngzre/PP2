names = ['Alice', 'Bob', 'Charlie']
scores = [85, 90, 78]

# enumerate()
print('Using enumerate():')
for index, name in enumerate(names, start=1):
    print(index, name)

# zip()
print('\nUsing zip():')
for name, score in zip(names, scores):
    print(f'{name}: {score}')

# Type checking and conversion
value = '123'
print('\nType before conversion:', type(value))
number = int(value)
print('Type after conversion:', type(number))
print('Converted value + 10 =', number + 10)

float_value = float('45.67')
print('Float conversion:', float_value)

list_to_tuple = tuple(names)
print('Tuple conversion:', list_to_tuple)
