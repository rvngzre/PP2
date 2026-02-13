class Counter:
    def __init__(self):
        self.value = 0
    def inc(self):
        self.value += 1

class Calculator:
    def add(self, a, b):
        return a + b

class TextTool:
    def upper(self, text):
        return text.upper()

class ListTool:
    def first(self, items):
        return items[0]

c = Counter()
c.inc()
print(c.value)

calc = Calculator()
print(calc.add(2, 3))

tool = TextTool()
print(tool.upper("hello"))

lt = ListTool()
print(lt.first([10, 20, 30]))
