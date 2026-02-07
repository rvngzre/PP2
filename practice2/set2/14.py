n = int(input())
a = list(map(int, input().split()))

freq = {}
for x in a:
    if x in freq:
        freq[x] += 1
    else:
        freq[x] = 1

best_num = None
best_cnt = -1

for num in freq:
    cnt = freq[num]
    if cnt > best_cnt:
        best_cnt = cnt
        best_num = num
    elif cnt == best_cnt and num < best_num:
        best_num = num

print(best_num)
