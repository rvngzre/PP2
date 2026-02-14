def isUsual(n):
    for d in [2, 3, 5]:
        while n % d == 0:
            n //= d
    return n == 1

n = int(input())
print("Yes" if isUsual(n) else "No")
