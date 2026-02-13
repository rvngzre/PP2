class Fly:
    def move(self):
        return "Fly"

class Swim:
    def swim(self):
        return "Swim"

class Walk:
    def walk(self):
        return "Walk"

class Duck(Fly, Swim, Walk):
    pass

d = Duck()
print(d.move())
print(d.swim())
print(d.walk())
print(type(d).__name__)
