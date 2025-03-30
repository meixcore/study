def insertion_sort(arr):
    for i in range(1, len(arr)):
        ind = i - 1
        elem = arr[i]

        while ind >= 0 and elem < arr[ind]:
            arr[ind + 1] = arr[ind]
            ind -= 1

        arr[ind + 1] = elem
    return arr

# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
insertion_sort(my_list)
print("Отсортированный список:", my_list)