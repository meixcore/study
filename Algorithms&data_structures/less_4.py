from stack_less_1 import Stack

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