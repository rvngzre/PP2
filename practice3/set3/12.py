class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_salary(self):
        return self.base_salary


class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus_percent = bonus_percent

    def total_salary(self):
        return self.base_salary * (1 + self.bonus_percent / 100)


class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.completed_projects = completed_projects

    def total_salary(self):
        return self.base_salary + self.completed_projects * 500


class Intern(Employee):
    pass


data = input().split()

role = data[0]
name = data[1]

if role == "Manager":
    base = int(data[2])
    bonus = int(data[3])
    emp = Manager(name, base, bonus)

elif role == "Developer":
    base = int(data[2])
    projects = int(data[3])
    emp = Developer(name, base, projects)

else: 
    base = int(data[2])
    emp = Intern(name, base)

print(f"Name: {emp.name}, Total: {emp.total_salary():.2f}")
