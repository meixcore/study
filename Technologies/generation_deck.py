import itertools

l1 = ['♠', '♥', '♦', '♣']
l2 = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

with open('combinations.txt', 'w', encoding='utf-8') as f:
    for c in itertools.product(l2, l1):
        f.write(''.join(c) + '\n')