import re

# Exercise 1
print("Exercise 1:")
s = input("Enter string: ")
if re.fullmatch(r"ab*", s):
    print("Match")
else:
    print("No match")


# Exercise 2
print("\nExercise 2:")
s = input("Enter string: ")
if re.fullmatch(r"ab{2,3}", s):
    print("Match")
else:
    print("No match")


# Exercise 3
print("\nExercise 3:")
s = input("Enter string: ")
print(re.findall(r"[a-z]+_[a-z]+", s))


# Exercise 4
print("\nExercise 4:")
s = input("Enter string: ")
print(re.findall(r"[A-Z][a-z]+", s))


# Exercise 5
print("\nExercise 5:")
s = input("Enter string: ")
if re.fullmatch(r"a.*b", s):
    print("Match")
else:
    print("No match")


# Exercise 6
print("\nExercise 6:")
s = input("Enter string: ")
print(re.sub(r"[ ,\.]", ":", s))


# Exercise 7
print("\nExercise 7:")
s = input("Enter snake_case string: ")
print(re.sub(r"_([a-z])", lambda x: x.group(1).upper(), s))


# Exercise 8
print("\nExercise 8:")
s = input("Enter string: ")
print(re.split(r"(?=[A-Z])", s))


# Exercise 9
print("\nExercise 9:")
s = input("Enter string: ")
print(re.sub(r"([A-Z])", r" \1", s).strip())


# Exercise 10
print("\nExercise 10:")
s = input("Enter camelCase string: ")
print(re.sub(r"([A-Z])", r"_\1", s).lower())