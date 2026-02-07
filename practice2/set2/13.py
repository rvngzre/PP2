x = int(input())

if x <= 1:
    print("No")
else:
    is_prime = True
    i = 2
    while i * i <= x:
        if x % i == 0:
            is_prime = False
            break
        i += 1

    print("Yes" if is_prime else "No")
