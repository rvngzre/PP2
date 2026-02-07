n, l, r = map(int, input().split())
a = list(map(int, input().split()))

left = l - 1
right = r - 1

while left < right:
    a[left], a[right] = a[right], a[left]
    left += 1
    right -= 1

print(*a)
