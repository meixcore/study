import json
import csv

def load_data_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_average_score(students):
    for student in students:
        student['avg'] = sum(student['grades'].values()) / len(student['grades'])
    return students

def get_best_student(students):
    return max(students, key=lambda x: x['avg'])

def get_worst_student(students):
    return min(students, key=lambda x: x['avg'])

def find_student(name, students):
    for student in students:
        if student['name'] == name:
            print(
                f'Имя: {student["name"]}\n'
                f'Возраст: {student["age"]}\n'
                f'Предметы: {student["subjects"]}\n'
                f'Оценки: {student["grades"]}'
            )
            return
    print('Студент с таким именем не найден')

def sorted_students(students):
    sort_stu = sorted(students, key=lambda x: x["avg"], reverse=True)
    print('Сортировка студентов по среднему баллу:')
    for stu in sort_stu:
        print(
            f'{stu["name"]}: {stu["avg"]}\n'
        )

def to_list(students):
    student_list = []
    for name, info in students.items():
        student = {'name': name}
        student.update(info)
        student_list.append(student)
    return student_list

def to_csv(filename, students):
    with open(filename, 'w', newline='', encoding='utf-8') as c:
        fieldnames = ['name', 'age', 'avg']
        writer = csv.DictWriter(c, fieldnames=fieldnames)
        writer.writeheader()

        for student in students:
            row = {field: student[field] for field in fieldnames}
            writer.writerow(row)

def main_1():
    stu = load_data_json(r'/Users/e.bubnikova/py/study/Technologies/student_list.json')
    student_list = to_list(stu)
    students = get_average_score(student_list)
    for s in students:
        print(f'Средний балл для студента {s["name"]}: {s["avg"]}')
    
    best_stu = get_best_student(students)
    print(f'Наилучший студент: {best_stu["name"]} (Средний балл: {best_stu["avg"]})')

    worst_stu = get_worst_student(students)
    print(f'Наихудший студент: {worst_stu["name"]} (Средний балл: {worst_stu["avg"]})')

    find_student('Emma', students)
    find_student('Ivan', students)

    sorted_students(students)
    to_csv('students_csv.csv', students)

    
    

main_1()