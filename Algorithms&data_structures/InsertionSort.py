def insertion_sort(arr):
    for j in range(1, len(arr)):
        for i in range(j, 0, -1):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]

    return arr

# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
insertion_sort(my_list)
print("Отсортированный список:", my_list)