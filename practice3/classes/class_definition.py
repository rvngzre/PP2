class User:
    def __init__(self, name):
        self.name = name
    def say_hello(self):
        print("Hello", self.name)

class Car:
    def __init__(self, brand):
        self.brand = brand
    def show(self):
        print("Car", self.brand)

class Book:
    def __init__(self, title):
        self.title = title
    def show(self):
        print("Book", self.title)

class Phone:
    def __init__(self, model):
        self.model = model
    def show(self):
        print("Phone", self.model)

User("Dana").say_hello()
Car("Toyota").show()
Book("Clean Code").show()
Phone("iPhone").show()
