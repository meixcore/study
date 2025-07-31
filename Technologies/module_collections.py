from collections import Counter, namedtuple, defaultdict, deque
import random

s = list(range(1, 21))
counter = Counter(random.choices(s, k=10))
print(counter)
print(Counter(counter).most_common(3))

Point = namedtuple('Book', ['title', 'author', 'genre'])
book1 = Point('Конец вечности', 'Азимов', 'Научная фантастика')
book2 = Point('Гарри Поттер', 'Роулинг', 'Фантастика')
book3 = Point('Снафф', 'Паланик', 'Роман')
print(
    f'Первая книга: {book1.title}, автор: {book1.author}, жанр: {book1.genre}\n'
    f'Вторая книга: {book2.title}, автор: {book2.author}, жанр: {book2.genre}\n'
    f'Третья книга: {book3.title}, автор: {book3.author}, жанр: {book3.genre}'
)

d = defaultdict(list)
d['a'].append('abc')
d['b'].append('cba')
d['a'].append('xyz')
print(d)

x = deque([1, 2, 3])
x.append(4)
print(x)
x.appendleft(0)
print(x)
x.pop()
print(x)
x.popleft()
print(x)

queue = deque()

def addqueue(q, item):
    q.append(item)

def dequeue(q):
    if q:
        return q.popleft()
    else:
        return None

addqueue(queue, 'первый')
addqueue(queue, 'второй')
addqueue(queue, 'третий')

print("Очередь после добавлений:", list(queue))

item = dequeue(queue)
print("Извлечено:", item)

print("Очередь после извлечения:", list(queue))