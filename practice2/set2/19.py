n = int(input())

total = {}
for _ in range(n):
    name, k = input().split()
    k = int(k)
    if name in total:
        total[name] += k
    else:
        total[name] = k

for name in sorted(total):
    print(name, total[name])
