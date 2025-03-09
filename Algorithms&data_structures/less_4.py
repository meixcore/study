class Stack:
    def __init__(self):
        self.items = []

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

def is_valid(s):
    s1 = Stack()
    for x, current_element in enumerate(s):
        if current_element == '(' or current_element == '[' or current_element == '{':
            s1.push(current_element)
            #print(f'добавили: {current_element}, index: {x}, список: {s1}')
        elif current_element == ')' and s1.items[-1] == '(':
            s1.pop()
            #print(f'убрали: {current_element}, index: {x}, список: {s1}')
        elif current_element == ']' and s1.items[-1] == '[':
            s1.pop()
            #print(f'убрали: {current_element}, index: {x}, список: {s1}')
        elif current_element == '}' and s1.items[-1] == '{':
            s1.pop()
            #print(f'убрали: {current_element}, index: {x}, cписок: {s1}')
        else:
            print('False. Строка является неправильной скобочной последовательностью')
            return False
    print('True. Строка является правильной скобочной последовательностью')
    return True

User_list = list(input('Введите скобочную последовательность: '))
is_valid(User_list)

# ([]{})
# ([)]
# {[}
# ()