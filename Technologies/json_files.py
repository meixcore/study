import json
import csv

def from_csv(file_name_csv):
    try:
        with open(file_name_csv, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=',')
            data = list(reader)
        return data
    except FileNotFoundError:
        print(f'Ошибка: {file_name_csv} - не найден.')
        return None

def to_json(file_name_json, data):
    with open(file_name_json, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    return json.dumps(data, ensure_ascii=False, indent=4)

def main():
    user_file_csv = input('Введите название csv файла для преобразования в json: ')
    data_csv = from_csv(user_file_csv)
    user_file_json = input('Введите название json файла: ')
    print(to_json(user_file_json, data_csv))

main()