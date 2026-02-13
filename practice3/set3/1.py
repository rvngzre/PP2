n = input()

valid = True
for d in n:
    if int(d) % 2 != 0:
        valid = False
        break

if valid:
    print("Valid")
else:
    print("Not valid")
