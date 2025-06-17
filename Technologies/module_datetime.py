import datetime

now = datetime.datetime.now()
print("Текущая дата и время:", now)
print(f'День недели: {now.strftime("%A")}, Номер дня недели: {now.strftime("%w")}')

year = datetime.datetime.now().year
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(f"{year} год — високосный")
else:
    print(f"{year} год — не високосный")

user_input = input("Введите дату в формате ГГГГ-ММ-ДД: ")
try:
    user_date = datetime.datetime.strptime(user_input, '%Y-%m-%d')
    now = datetime.datetime.now()
    difference = user_date - now

    if difference.total_seconds() < 0:
        print('Эта дата уже прошла')
    else:
        total_seconds = int(difference.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60

        print(f'До {user_input} осталось: {days} дней, {hours} часов, {minutes} минут.')

except ValueError:
    print('Некорректный формат')