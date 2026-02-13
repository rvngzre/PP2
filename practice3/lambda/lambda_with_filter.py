nums = list(range(1, 11))
even_nums = list(filter(lambda x: x % 2 == 0, nums))

words = ["hi", "hello", "amazing"]
long_words = list(filter(lambda w: len(w) > 5, words))

values = [10, -2, 3, 0]
positive = list(filter(lambda v: v > 0, values))

not_zero = list(filter(lambda v: v != 0, values))

print(even_nums)
print(long_words)
print(positive)
print(not_zero)
