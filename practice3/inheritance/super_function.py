class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, major):
        super().__init__(name)
        self.major = major

class Worker(Person):
    def __init__(self, name, job):
        super().__init__(name)
        self.job = job

class Player(Person):
    def __init__(self, name, game):
        super().__init__(name)
        self.game = game

s = Student("Dana", "SE")
w = Worker("Ayan", "Dev")
p = Player("Ali", "CS2")
base = Person("Asel")

print(s.name, s.major)
print(w.name, w.job)
print(p.name, p.game)
print(base.name)
