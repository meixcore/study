from functools import reduce

def cubed(x):
    return x ** 3

numbers = [1, 2, 3, 4, 5]
cube = list(map(cubed, numbers))
print(cube)

def division_5(x):
    return x % 5 == 0

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
division_5_numbers = list(filter(division_5, numbers))
print(division_5_numbers)

def is_odd(x):
    return x % 2 != 0

def multiply(a, b):
    return a * b

odds = filter(is_odd, numbers)
print(reduce(multiply, odds))