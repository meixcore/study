import requests
from datetime import datetime

#1
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        t_start = datetime.now()
        result = func(*args, **kwargs)
        t_finish = datetime.now()
        execution_time = t_finish - t_start
        milliseconds = round(execution_time.microseconds / 1000)
        print(f"Function completed in {execution_time.seconds}s {milliseconds}ms")
        return result
    return wrapper

@measure_execution_time
def count_http(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при запросе к {url}: {e}")
        return None

url1 = 'https://www.google.com'
count_http(url1)

#2
def requires_admin(func):
    def wrapper(user, *args, **kwargs):
        if user.get('role') != 'admin':
            raise PermissionError("У вас нет прав для выполнения этой операции.")
        return func(user, *args, **kwargs)
    return wrapper

@requires_admin
def delete_user(user, username_to_delete):
    return f"User {username_to_delete} has been deleted by {user['username']}."

# Пример юзеров
admin_user = {'username': 'Alice', 'role': 'admin'}
regular_user = {'username': 'Bob', 'role': 'user'}

# Вызовы функции
print(delete_user(admin_user, 'Charlie')) # Должно отработать
print(delete_user(regular_user, 'Charlie')) # Должно рейзить PermissionError