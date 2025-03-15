class Deque:
    def __init__(self):
        self.items = []

    def add_front(self, item):
        self.items.insert(0, item)

    def add_rear(self, item):
        self.items.append(item)

    def remove_front(self):
        if not self.is_empty():
            return self.items.pop(0)
        else:
            raise IndexError("Двусторонняя очередь пуста")

    def is_empty(self):
        return len(self.items) == 0

    def remove_rear(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("Двусторонняя очередь пуста")

    def size(self):
        return len(self.items)

    def display(self):
        return list(self.items)

# Создаем экземпляр двусторонней очереди
deque = Deque()

# Визуализируем добавление элементов
deque.add_front(1)
print("Очередь после добавления 1 в начало:", deque.display())

deque.add_rear(2)
print("Очередь после добавления 2 в конец:", deque.display())

deque.add_front(3)
print("Очередь после добавления 3 в начало:", deque.display())

# Визуализируем извлечение элементов
front_element = deque.remove_front()
print("Извлечен элемент с начала:", front_element)
print("Очередь после извлечения с начала:", deque.display())

rear_element = deque.remove_rear()
print("Извлечен элемент с конца:", rear_element)
print("Очередь после извлечения с конца:", deque.display())

print("Очередь пуста:", deque.is_empty())

# from collections import deque

# # Создание двусторонней очереди
# deque_queue = deque()
#
# # Добавление элементов в начало и конец очереди
# deque_queue.appendleft(1)   # Добавление в начало
# deque_queue.append(2)      # Добавление в конец
#
# # Извлечение элементов с начала и конца очереди
# front_element = deque_queue.popleft()  # Извлечение с начала
# rear_element = deque_queue.pop()        # Извлечение с конца
#
# print("Front Element:", front_element)
# print("Rear Element:", rear_element)