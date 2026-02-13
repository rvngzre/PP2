nums = [1, 2, 3]
squares = list(map(lambda x: x * x, nums))

words = ["hi", "hello"]
lengths = list(map(lambda w: len(w), words))

prices = [100, 200]
sale = list(map(lambda p: p * 0.9, prices))

bigger = list(map(lambda x: x + 10, nums))

print(squares)
print(lengths)
print(sale)
print(bigger)
