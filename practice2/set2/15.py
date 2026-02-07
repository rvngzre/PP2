n = int(input())

seen = set()
for i in range(n):
    name = input().strip()
    seen.add(name)

print(len(seen))
