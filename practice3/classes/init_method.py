class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Timer:
    def __init__(self, seconds=0):
        self.seconds = seconds

class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa

class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.area = w * h

p = Point(2, 3)
t = Timer(120)
s = Student("Ayan", 3.6)
r = Rectangle(4, 5)

print(p.x, p.y)
print(t.seconds)
print(s.name, s.gpa)
print(r.area)
