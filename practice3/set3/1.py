n = int(input())

def is_valid_number(n):
    n = abs(n)
    for digit in str(n):
        if int(digit) % 2 != 0:
            print("Not Valid")
            return
    print("Valid")

is_valid_number(n)
