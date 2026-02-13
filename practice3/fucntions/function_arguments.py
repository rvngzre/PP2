def area(w, h):
    return w * h

def greet(name, text="Hello"):
    return text + " " + name

def order(item, count=1):
    return item + " " + str(count)

def info(name, age=18, city="Astana"):
    return name + " " + str(age) + " " + city

print(area(4, 5))
print(greet("Dana"))
print(order("Burger", 2))
print(info("Ayan", 19, "Almaty"))
