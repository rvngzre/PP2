n = int(input())

seen = set()
for _ in range(n):
    name = input().strip()
    seen.add(name)

print(len(seen))
