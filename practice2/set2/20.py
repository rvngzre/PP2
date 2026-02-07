n = int(input())
doc = {}

for i in range(n):
    parts = input().split()
    cmd = parts[0]

    if cmd == "set":
        key = parts[1]
        value = parts[2]
        doc[key] = value
    else:  
        key = parts[1]
        if key in doc:
            print(doc[key])
        else:
            print("KE: no key " + key + " found in the document")
