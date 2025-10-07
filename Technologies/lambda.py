#1
strings = ["apple", "kiwi", "banana", "fig"]
filter_strings = list(filter(lambda x: len(x) > 4, strings))
print(filter_strings)

#2
students = [
    {"name": "John", "grade": 90},
    {"name": "Jane", "grade": 85},
    {"name": "Dave", "grade": 92}
]
print(max(students, key=lambda x: x['grade']))

#3
tuples = [(1, 5), (3, 2), (2, 8), (4, 3)]
print(sorted(tuples, key=lambda x: sum(x)))

#4
spisok = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(list(filter(lambda x: x % 2 == 0, spisok)))

#5
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __repr__(self):
        return f'Person(name={self.name}, age={self.age}'

persons = [
    Person("John", 20),
    Person("Jane", 25),
    Person("Dave", 22)
]

print(sorted(persons, key=lambda x: x.age))