import json
import csv


#Создаем файлы для заданий
#
# for_json = [
#     {"имя": "Анна", "возраст": 20, "город": "Москва", "предметы": ["Python", "JavaScript"]},
#     {"имя": "Петр", "возраст": 22, "город": "Санкт-Петербург", "предметы": ["Python", "Java"]},
#     {"имя": "Мария", "возраст": 21, "город": "Киев", "предметы": ["JavaScript", "SQL"]}
# ]
#
# with open('students.json', 'w', encoding='utf-8') as json_file:
#     json.dump(for_json, json_file, ensure_ascii=False, indent=4)
#
# for_csv = [
#     {'Дата': '2023-01-01', 'Продукт': 'Продукт A', 'Сумма': '500'},
#     {'Дата': '2023-02-15', 'Продукт': 'Продукт B', 'Сумма': '700'},
#     {'Дата': '2023-03-10', 'Продукт': 'Продукт A', 'Сумма': '800'},
#     {'Дата': '2023-04-05', 'Продукт': 'Продукт C', 'Сумма': '600'},
#     {'Дата': '2023-04-20', 'Продукт': 'Продукт B', 'Сумма': '900'},
#     {'Дата': '2023-05-12', 'Продукт': 'Продукт A', 'Сумма': '1000'}
# ]
#
# with open('sales.csv', 'w', encoding='utf-8', newline='') as csv_file:
#     fieldsnames = ['Дата', 'Продукт', 'Сумма']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldsnames)
#
#     writer.writeheader()
#     writer.writerows(for_csv)
#
# for_json2 = [
#     {"id": 1, "имя": "Иван", "должность": "Менеджер"},
#     {"id": 2, "имя": "Елена", "должность": "Аналитик"},
#     {"id": 3, "имя": "Дмитрий", "должность": "Разработчик"}
# ]
#
# with open('employees.json', 'w', encoding='utf-8') as json_file:
#     json.dump(for_json2, json_file, ensure_ascii=False, indent=4)
#
# for_csv2 = [
#     {'emploee_id': '1', 'performance': '85'},
#     {'emploee_id': '2', 'performance': '92'},
#     {'emploee_id': '3', 'performance': '78'}
# ]
#
# with open('performance.csv', 'w', encoding='utf-8', newline='') as csv_file:
#     fieldsnames = ['emploee_id', 'performance']
#     writer = csv.DictWriter(csv_file, fieldnames=fieldsnames)
#
#     writer.writeheader()
#     writer.writerows(for_csv2)

def load_data_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def search_oldest_student(students):
    old_student = students[0]
    for student in students:
        if student['возраст'] > old_student['возраст']:
            old_student = student
    return old_student

def main_1():
    data_students = load_data_json('students.json')
    print(f'Общее кол-во студентов: {len(data_students)}')

    old_student = search_oldest_student(data_students)
    print(f'Самый взрослый студент:\n'
          f'Имя: {old_student['имя']}\n'
          f'Возраст: {old_student['возраст']}\n'
          f'Город: {old_student['город']}')

    skill = 'Python'
    python_students = [s for s in data_students if skill in s['предметы']]
    print(f'Количество студентов, изучающих {skill}: {len(python_students)}')

main_1()

def load_data_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=',')
        data = list(reader)
    return data

def calc_total(data):
    totals = {}
    for row in data:
        product = row['Продукт']
        amount = int(row['Сумма'])
        totals[product] = totals.get(product, 0) + amount
    return totals

def main_2():
    data_csv = load_data_csv('sales.csv')
    total_sum = sum(int(s['Сумма']) for s in data_csv)
    print(f'Сумма всех продуктов: {total_sum}')
    totals = calc_total(data_csv)
    max_amount = max(totals, key=totals.get)
    print(f'Продукт с макс суммой продаж: {max_amount} = {totals[max_amount]}')

main_2()

def merge_data(employees, performance_list):
    for emp in employees:
        emp_id = int(emp['id'])
        emp['performance'] = performance_list.get(emp_id)
    return employees

def read_csv_to_dict(filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[int(row['emploee_id'])] = int(row['performance'])
    return data

def average_performance(workers):
    summary_workers = 0
    count = 0
    for worker in workers:
        summary_workers += worker['performance']
        count += 1
    return summary_workers / count

def max_performance(workers):
    best_worker = None
    for worker in workers:
        if best_worker is None or worker['performance'] > best_worker['performance']:
            best_worker = worker
    return best_worker

def main_3():
    data_csv = read_csv_to_dict('performance.csv')
    data_json = load_data_json('employees.json')
    merged = merge_data(data_json, data_csv)
    print(f'Средняя производительность сотрудников: {average_performance(merged)}')
    best_work = max_performance(merged)
    print(f'Лучший сотрудник: {best_work['имя']} - {best_work['performance']}')

main_3()