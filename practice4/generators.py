#exercise1
def square(n):
    for i in range(1, n+1):
        yield i * i
N = int(input())
for i in square(N):
    print(i)

#exercise2
def even(n):
    for i in range(0,n+1):
        if i%2==0:
            yield i
N = int(input())
print(",".join(str(num) for num in even(N)))

#exercise3

def divisible_by3_by4(n):
    for i in range(0, n+1):
        if i%3==0 and i%4==0:
            yield i
N = int(input())
for i in divisible_by3_by4(N):
    print(i)

#exercise4
def squares(a, b):
    for i in range(a, b+1):
        yield i * i
a = int(input())
b = int(input())
for i in squares(a,b):
    print(i)

#exercise5
def countdown(n):
    for i in range(n, -1,-1): #stop at 0(inclusive)
        yield i
N = int(input())
for i in countdown(N):
    print(i)