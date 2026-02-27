#exercise1
import math
degree = float(input("Input degree: "))
radian = math.radians(degree)
print("Output radian:", format(radian, ".6f")) #6 decimal output

#exercise2
height = int(input("Height: "))
base1 = int(input("Base, first value: "))
base2 = int(input("Base, second value: "))
area = ((base1 + base2) * height)/2
print("Expected Output:",area) 


#with import math
import math

height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))

area = math.fsum([base1, base2]) * height / 2

print("Expected Output:", area)

#exercise3
import math
number_sides = int(input("Input number of sides: "))
length_sides = int(input("Input the length of a side: "))
area = (number_sides*length_sides**2)/(4*math.tan(math.pi/number_sides))
print("The area of the polygon is:", int(area))

#exercise4
import math
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area = math.prod([base, height]) #product of iterables
print("Expected Output:", area)