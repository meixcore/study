def merge_sort(arr):
    # Шаг 1: Проверяем, если длина массива больше 1, то продолжаем сортировку
    if len(arr) > 1:
        middle = len(arr) // 2  # Находим средний индекс массива
        left_half = arr[:middle]  # Делим массив на две половины: левую и правую
        right_half = arr[middle:]

        # Шаг 2: Рекурсивно сортируем обе половины
        merge_sort(left_half)
        merge_sort(right_half)

        # Шаг 3: Слияние (merge) отсортированных половин
        i = j = k = 0  # Индексы для левой, правой и общей частей массива

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Если в одной из половин остались элементы, добавляем их в конец
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
merge_sort(my_list)
print("Отсортированный список:", my_list)