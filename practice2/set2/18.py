n = int(input())
arr = []

for x in range(n):
    arr.append(input().strip())

first_pos = {}
for i in range(n):
    s = arr[i]
    if s not in first_pos:
        first_pos[s] = i + 1

for s in sorted(first_pos):
    print(s, first_pos[s])
