n = int(input())

freq = {}
for _ in range(n):
    phone = input().strip()
    if phone in freq:
        freq[phone] += 1
    else:
        freq[phone] = 1

ans = 0
for phone in freq:
    if freq[phone] == 3:
        ans += 1

print(ans)
