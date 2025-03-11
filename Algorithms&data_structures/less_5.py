from stack_less_1 import Stack

def calc(s):
    s1 = Stack()
    tokens = s.split()
    # print(tokens)
    for token in tokens:
        if token.isdigit():
            s1.push(int(token))
            # print(s1)
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
            raise ValueError('Символ не цифра и не "+-*/"')
        print(f'{s1.items[0]}')

x = input('Введите выражение для вычисления: ')
calc(x)

# 3 4 2 * +     25 11 +