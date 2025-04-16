import csv

def txt_dict(filename):
    for_csv = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            name, count, cost = line.strip().split('\t')
            item = {
                'Наименование товара': name,
                'Количество': int(count),
                'Цена за 1 шт': int(cost)
            }
            for_csv.append(item)
    return for_csv


def create_csv(filename, for_csv):
    with open(filename, 'w', newline='', encoding='utf-8') as c:
        fieldnames = ['Наименование товара', 'Количество', 'Цена за 1 шт']
        writer = csv.DictWriter(c, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(for_csv)

    print('Данные успешно записаны в csv')


def cost_for_all(csv_data):
    total = 0
    with open(csv_data, 'r', newline='', encoding='utf-8') as c:
        reader = csv.DictReader(c)
        for row in reader:
            count = int(row['Количество'])
            cost = int(row['Цена за 1 шт'])
            total += count * cost
        return total


def main():
    user_file = input('Введите название файла для преобразования в csv: ')
    dict_for_csv = txt_dict(user_file)
    create_csv('prices.csv', dict_for_csv)
    print('Общая сумма:', cost_for_all('prices.csv'))

main()