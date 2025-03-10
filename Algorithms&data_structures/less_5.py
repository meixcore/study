from stack_less_1 import Stack

def calc(s):
    s1 = Stack()
    tokens = s.split()
    for token in tokens:
        if token in '1234567890':
            s1.push(int(token))
        elif token == '+':
            plus = s1.items[-1] + s1.items[-2]
            s1.pop()
            s1.pop()
            s1.push(plus)
        elif token == '-':
            minus = s1.items[-1] + s1.items[-2]
            s1.pop()
            s1.pop()
            s1.push(minus)
        elif token == '*':
            umn = s1.items[-1] * s1.items[-2]
            s1.pop()
            s1.pop()
            s1.push(umn)
        elif token == '/':
            delen = s1.items[-1] / s1.items[-2]
            s1.pop()
            s1.pop()
            s1.push(delen)
        else:
            raise ValueError('Ошибка')
        print(f'{s1.items[0]}')

x = input('Введите выражение для вычисления: ')
calc(x)