def sum_all(*nums):
    return sum(nums)

def profile(**data):
    return data

def show(name, *tags):
    print(name, tags)

def multiply(a, b, c):
    return a * b * c

print(sum_all(1, 2, 3))
print(profile(name="Dana", age=20))
show("login", "user", "ok")
print(multiply(2, 3, 4))
