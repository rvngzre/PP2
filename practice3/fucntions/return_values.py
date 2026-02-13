def to_f(c):
    return c * 9 / 5 + 32

def min_max(nums):
    return min(nums), max(nums)

def divide(a, b):
    if b == 0:
        return None
    return a / b

def get_word():
    return "Python"

print(to_f(20))
print(min_max([1, 5, 3]))
print(divide(10, 2))
print(get_word())
