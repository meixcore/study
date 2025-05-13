text_file = open('data.txt', 'w', encoding='utf-8')
text_file.write(
    'Проснулся в два часа дня, потому что мозг — это ночной клаббер, а не орган мышления. '
    'Поставил будильник на семь — просто чтобы узнать, каково чувствовать предательство от самого себя. '
    'Пока мыл кружку, понял, что это уже вторая в этом году — пора брать ипотеку. Жизнь — не симулятор, но графика '
    'реалистичная и багов хватает.'
)
text_file.close()

def get_words(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()

    punctuation = '.,!?;:-()[]{}"«»—…'

    for ch in punctuation:
        text = text.replace(ch, '')

    text = text.replace('\n', ' ')
    words = text.lower().split()
    return words

def get_words_dict(words):
    dict_words = {}
    for i in words:
        if i in dict_words:
            dict_words[i] += 1
        else:
            dict_words[i] = 1
    return dict_words

def main():
    all_words = get_words(input('Введите название файла: '))
    words_dict = get_words_dict(all_words)

    print(f'Кол-во слов: {sum(words_dict.values())}\n'
          f'Кол-во уникальных слов: {len(words_dict)}\n'
          f'Все использованные слова:')

    for word, value in sorted(words_dict.items()):
        print(f'{word} {value}')

main()