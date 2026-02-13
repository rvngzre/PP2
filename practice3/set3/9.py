class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius * self.radius


r = int(input())
c = Circle(r)
a = c.area()

print(f"{a:.2f}")
