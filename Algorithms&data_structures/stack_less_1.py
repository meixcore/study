class Stack:
    def __init__(self) -> None:
        self.items: list[int] = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError('Стек пуст')

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError('Стек пуст')

    def size(self):
        return len(self.items)

    def __str__(self):
        return f'{self.items}'

# my_stack = Stack()
# my_stack.push(5)
# my_stack.push(10)
# my_stack.push(15)
#
# print("Вершина стека:", my_stack.peek())
# my_stack.pop()
# print("Стек пуст?", my_stack.is_empty())
# print("Размер стека:", my_stack.size())
