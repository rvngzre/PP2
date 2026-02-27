N = int(input())

p = 1
ans = []
while p <= N:
    ans.append(p)
    p *= 2

print(*ans)
