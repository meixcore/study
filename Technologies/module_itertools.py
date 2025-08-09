import itertools
from itertools import cycle, islice, chain, permutations

#1
x = itertools.combinations([1, 2, 3, 4], 2)
print(list(x))

#2
y = 'Python'
all = permutations(y)
for a in all:
    print(''.join(a))

#3
a = ['a', 'b']
b = [1, 2, 3]
c = ['x', 'y']
abc = list(chain(a, b, c))
print(list(islice(cycle(abc), 35)))

#4
def fib(n):
    numbers = []
    a, b = 0, 1
    for i in range(n):
        numbers.append(a)
        a, b = b, a + b
    return numbers

print(fib(10))

#5
l1 = ['red', 'blue']
l2 = ['shirt', 'shoes']
for s in itertools.product(l1, l2):
    print(' '.join(s))