class Student:
    count = 0
    def __init__(self, name):
        self.name = name
        Student.count += 1

class Car:
    wheels = 4
    def __init__(self, brand):
        self.brand = brand

class App:
    version = "1.0"
    def __init__(self, name):
        self.name = name

class Device:
    type = "Electronics"
    def __init__(self, name):
        self.name = name

Student("Ayan")
Student("Dana")
print(Student.count)

c = Car("BMW")
print(Car.wheels)

a = App("Chat")
print(App.version)

d = Device("Laptop")
print(Device.type)
