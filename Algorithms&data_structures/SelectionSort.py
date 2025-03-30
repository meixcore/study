def selection_sort(arr):
    for j in range(len(arr) - 1):
        elem = arr[j] #min
        ind = j
        for i in range(j + 1, len(arr)):
            if elem > arr[i]:
                elem = arr[i]
                ind = i
        if ind != j:
            arr[j], arr[ind] = arr[ind], arr[j]

# Пример использования:
my_list = [64, 34, 25, 12, 22, 11, 90]
selection_sort(my_list)
print("Отсортированный список:", my_list)