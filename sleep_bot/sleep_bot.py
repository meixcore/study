import os
import telebot
import time
import json
from dotenv import load_dotenv
from sqlite3 import connect

load_dotenv()
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
user_sleep_data = {}

#Таблица users хранит информацию о пользователях, включая их уникальные Telegram ID и имена.
conn = connect("users.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
    """
)
conn.commit()
conn.close()


#Таблица sleep_record хранит информацию о ежедневных записях о сне пользователей, 
#включая время начала и окончания сна, а также оценку качества сна.
conn = connect("sleep_records.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS sleep_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INT,
        sleep_time DATETIME,
        wake_time DATETIME DEFAULT NULL,
        sleep_quality INT DEFAULT NULL
    );
    """
)
conn.commit()
conn.close()

#Таблица notes хранит текстовые заметки, которые пользователи могут добавлять к своим записям о сне.
conn = connect("notes.db")
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        sleep_record_id INT
    );
    """
)
conn.commit()
conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    new_user(message.from_user.id, message.from_user.username)
    bot.send_message(message.from_user.id, 'Привет! Давай улучшать качество сна🥰\nИспользуй команды '
                                           '/sleep, /wake, /quality и /notes.')


@bot.message_handler(commands=['sleep'])
def sleep(message):
    user_id = message.from_user.id
    sleep_time = time.time()
    sleep_id = save_sleep_time(user_id, sleep_time)

    user_sleep_data.setdefault(user_id, []).append({
        'sleep_time': time.time(),
        'sleep_id': sleep_id,
        'duration': None,
        'quality': None,
        'notes': None
    })
    
    bot.send_message(user_id, 'Доброй ночи! Не забудь сообщить мне, когда проснешься командой /wake')

@bot.message_handler(commands=['wake'])
def wake(message):
    user_id = message.from_user.id
    sleep_id = user_sleep_data[user_id][-1]['sleep_id']

    if user_sleep_data[user_id][-1]['sleep_time'] is not None:
        wake_time = time.time()
        sleep_duration = wake_time - user_sleep_data[user_id][-1]['sleep_time']
        hours = int(sleep_duration // 3600)
        minutes = int((sleep_duration % 3600) // 60)
        user_sleep_data[user_id][-1]['duration'] = sleep_duration

        save_wake_time(sleep_id, wake_time)
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
    sleep_id = user_sleep_data[user_id][-1]['sleep_id']
    try:
        quality_score = int(message.text)
        if 1 <= quality_score <= 5:
            user_sleep_data[user_id][-1]['quality'] = quality_score
            bot.send_message(message.chat.id, 'Спасибо за оценку. Теперь можешь добавить заметки командой /notes')
            save_sleep_quality(sleep_id, quality_score)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите оценку от 1 до 5.')
            bot.register_next_step_handler(message, process_quality_step)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение оценки.')
        bot.register_next_step_handler(message, process_quality_step)

@bot.message_handler(commands=['notes'])
def notes(message):
    user_id = message.from_user.id

    if user_id not in user_sleep_data or not user_sleep_data[user_id]:
        bot.send_message(message.chat.id, 'Сначала используй команду /sleep перед тем как оставить заметки.')
        return

    bot.send_message(message.chat.id, 'Введите заметки о вашем сне:')
    bot.register_next_step_handler(message, process_notes_step)


def process_notes_step(message):
    user_id = message.from_user.id
    notes = message.text
    sleep_id = user_sleep_data[user_id][-1]['sleep_id']

    save_notes(notes, sleep_id)

    user_sleep_data[user_id][-1]['notes'] = notes
    bot.send_message(message.chat.id, 'Заметки сохранены!')

    if user_sleep_data[user_id][-1]['quality'] is not None:
        bot.send_message(message.chat.id, f'Все данные сна зафиксированы. Качество сна: '
                                          f'{user_sleep_data[user_id][-1]['quality']}. '
                                          f'Заметки: {all_notes(sleep_id)}')

def new_user(user_id, username):
    conn = connect("users.db")
    cursor = conn.cursor()
    
    cursor.execute(
        """
        INSERT OR IGNORE INTO users (id, name) 
        VALUES (?, ?);
        """,
        (user_id, username)
    )
    conn.commit()
    conn.close()

def save_sleep_time(user_id, sleep_time):
    conn = connect("sleep_records.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO sleep_records (user_id, sleep_time) 
        VALUES (?, ?);
        """,
        (user_id, sleep_time)
    )
    conn.commit()
    sleep_record_id = cursor.lastrowid
    conn.close()
    return sleep_record_id

def save_wake_time(sleep_id, wake_time):
    conn = connect("sleep_records.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE sleep_records
        SET wake_time = ?
        WHERE id = ?
        """,
        (wake_time, sleep_id)
    )
    conn.commit()
    conn.close()

def save_sleep_quality(sleep_id, quality_score):
    conn = connect("sleep_records.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE sleep_records
        SET sleep_quality = ?
        WHERE id = ?
        """,
        (quality_score, sleep_id)
    )
    conn.commit()
    conn.close()

def save_notes(text, sleep_record_id):
    conn = connect("notes.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notes (text, sleep_record_id) 
        VALUES (?, ?);
        """,
        (text, sleep_record_id)
    )
    conn.commit()
    conn.close()

def all_notes(sleep_record_id):
    conn = connect("notes.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT text FROM notes
        WHERE sleep_record_id = ?
        """,
        (sleep_record_id,)
    )
    texts = cursor.fetchall()
    conn.close()

    return [text for (text,) in texts]

bot.polling(non_stop=True, interval=0)