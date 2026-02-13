words = ["banana", "kiwi", "apple"]
by_len = sorted(words, key=lambda w: len(w))

nums = [2, 15, 9]
near10 = sorted(nums, key=lambda x: abs(x - 10))

items = [{"price": 5}, {"price": 2}, {"price": 8}]
by_price = sorted(items, key=lambda x: x["price"])

pairs = [("Ayan", 3.2), ("Dana", 3.8), ("Ali", 3.5)]
by_score = sorted(pairs, key=lambda p: p[1], reverse=True)

print(by_len)
print(near10)
print(by_price)
print(by_score)
