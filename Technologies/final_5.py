import json

def load_data_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_average_score(data):


def main_1():
    students = load_data_json('students_list.json')
