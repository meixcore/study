import os
import telebot
import time
import json

bot = telebot.TeleBot(os.getenv('bot'))
user_sleep_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, 'Привет! Давай улучшать качество сна🥰\nИспользуй команды '
                                           '/sleep, /wake, /quality и /notes.')

@bot.message_handler(commands=['sleep'])
def sleep(message):
    user_id = message.from_user.id

    user_sleep_data.setdefault(user_id, []).append({
        'sleep_time': time.time(),
        'duration': None,
        'quality': None,
        'notes': None
    })
    save_data()
    bot.send_message(message.from_user.id, 'Споки! Не забудь сообщить мне, когда проснешься командой /wake')

@bot.message_handler(commands=['wake'])
def wake(message):
    user_id = message.from_user.id

    if user_sleep_data[user_id][-1]['sleep_time'] is not None:
        wake_time = time.time()
        sleep_duration = wake_time - user_sleep_data[user_id][-1]['sleep_time']
        hours = int(sleep_duration // 3600)
        minutes = int((sleep_duration % 3600) // 60)
        user_sleep_data[user_id][-1]['duration'] = sleep_duration
        save_data()
        bot.send_message(message.chat.id,
                         f'Ты проспал {hours} ч. {minutes} мин. Не забудь оценить качество сна командой '
                         f'/quality и оставить заметки командой /notes')
    else:
        bot.send_message(message.chat.id, 'Сначала используй команду /sleep перед тем как зафиксировать время сна!')

@bot.message_handler(commands=['quality'])
def quality(message):
    user_id = message.from_user.id
    if user_sleep_data[user_id][-1]['quality'] is None:
        bot.send_message(message.chat.id, 'Оцени качество сна от 1 до 5')
        bot.register_next_step_handler(message, process_quality_step)
    else:
        bot.send_message(message.chat.id, 'Сначала используй команду /sleep перед тем как оценить качество сна.')

def process_quality_step(message):
    user_id = message.from_user.id
    try:
        quality_score = int(message.text)
        if 1 <= quality_score <= 5:
            user_sleep_data[user_id][-1]['quality'] = quality_score
            save_data()
            bot.send_message(message.chat.id, 'Спасибо за оценку. Теперь можешь добавить заметки командой /notes')
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите оценку от 1 до 5.')
            bot.register_next_step_handler(message, process_quality_step)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение оценки.')
        bot.register_next_step_handler(message, process_quality_step)

@bot.message_handler(commands=['notes'])
def notes(message):
    user_id = message.from_user.id
    if user_sleep_data[user_id][-1]['notes'] is None:
        bot.send_message(message.chat.id, 'Введите заметки о вашем сне:')
        bot.register_next_step_handler(message, process_notes_step)
    else:
        bot.send_message(message.chat.id, 'Сначала используй команду /sleep перед тем как оставить заметки.')


def process_notes_step(message):
    user_id = message.from_user.id
    user_sleep_data[user_id][-1]['notes'] = message.text
    bot.send_message(message.chat.id, 'Заметки сохранены!')
    if user_sleep_data[user_id][-1]['quality'] is not None:
        print(user_sleep_data[user_id]) # оставила для проверки
        bot.send_message(message.chat.id, f'Все данные сна зафиксированы. Качество сна: '
                                          f'{user_sleep_data[user_id][-1]['quality']}. '
                                          f'Заметки: {user_sleep_data[user_id][-1]['notes']}')

def save_data():
    with open('sleep_data.json', 'w') as f:
        json.dump(user_sleep_data, f)

bot.polling(non_stop=True, interval=0)