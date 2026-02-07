n = int(input())
a = list(map(int, input().split()))

cnt = 0
for x in a:
    if x > 0:
        cnt += 1

print(cnt)
