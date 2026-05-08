import os
import telebot
import time
from dotenv import load_dotenv
from sqlite3 import connect

load_dotenv()
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN не найден")

bot = telebot.TeleBot(TOKEN)
user_sleep_data = {}

conn = connect("sleep_bot.db")
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
    active_sleep = get_active_sleep(user_id)

    if active_sleep is not None:
        bot.send_message(user_id, 'У тебя уже есть активный сон. Если хочешь закончить его, то нажми /wake')
    else:
        sleep_time = time.time()
        save_sleep_time(user_id, sleep_time)
        bot.send_message(user_id, 'Доброй ночи! Не забудь сообщить мне, когда проснешься командой /wake')
    

@bot.message_handler(commands=['wake'])
def wake(message):
    user_id = message.from_user.id
    sleep_time = get_active_sleep(user_id)

    if sleep_time is not None:
        wake_time = time.time()
        sleep_duration = wake_time - sleep_time
        hours = int(sleep_duration // 3600)
        minutes = int((sleep_duration % 3600) // 60)

        save_wake_time(user_id, wake_time)
        bot.send_message(message.chat.id,
                         f'Ты проспал {hours} ч. {minutes} мин. Не забудь оценить качество сна командой '
                         f'/quality и оставить заметки командой /notes')
    else:
        bot.send_message(message.chat.id, 'Сначала используй команду /sleep перед тем как зафиксировать время сна!')

@bot.message_handler(commands=['quality'])
def quality(message):
    user_id = message.from_user.id

    if get_quality(user_id) is None:
        bot.send_message(message.chat.id, 'Оцени качество сна от 1 до 5')
        bot.register_next_step_handler(message, process_quality_step)
    else:
        bot.send_message(message.chat.id, 'Оценка прошлого сна уже есть. Сначала используй команду /sleep перед тем как оценить качество нового сна.')

def process_quality_step(message):
    user_id = message.from_user.id
    try:
        quality_score = int(message.text)
        if 1 <= quality_score <= 5:
            bot.send_message(message.chat.id, 'Спасибо за оценку. Теперь можешь добавить заметки командой /notes')
            save_sleep_quality(user_id, quality_score)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введите оценку от 1 до 5.')
            bot.register_next_step_handler(message, process_quality_step)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите числовое значение оценки.')
        bot.register_next_step_handler(message, process_quality_step)

@bot.message_handler(commands=['notes'])
def notes(message):
    user_id = message.from_user.id

    if get_sleep_id(user_id) is not None:
        bot.send_message(message.chat.id, 'Введите заметки о вашем сне:')
        bot.register_next_step_handler(message, process_notes_step)
    else:
        bot.send_message(message.chat.id, 'У вас нет записей о снах')


def process_notes_step(message):
    user_id = message.from_user.id
    notes = message.text
    sleep_id = get_sleep_id(user_id)

    save_notes(notes, sleep_id)
    bot.send_message(message.chat.id, 'Заметки сохранены!')

    if sleep_id is not None:
        bot.send_message(message.chat.id, f'Все данные сна зафиксированы. Качество сна: '
                                          f'{get_quality(user_id)}. '
                                          f'Заметки: {all_notes(sleep_id)}')

def new_user(user_id, username):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR IGNORE INTO users (id, name) 
            VALUES (?, ?);
            """,
            (user_id, username)
        )


def save_sleep_time(user_id, sleep_time):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO sleep_records (user_id, sleep_time) 
            VALUES (?, ?);
            """,
            (user_id, sleep_time)
        )
        sleep_record_id = cursor.lastrowid
    return sleep_record_id

def get_active_sleep(user_id):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sleep_time FROM sleep_records
            WHERE user_id = ? AND wake_time IS NULL
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )
        result = cursor.fetchone()

    if result is None:
        return None

    return result[0]

def get_quality(user_id):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT sleep_quality FROM sleep_records
            WHERE user_id = ? AND wake_time IS NOT NULL
            ORDER BY wake_time DESC
            LIMIT 1
            """,
            (user_id,)
        )
        result = cursor.fetchone()

    if result is None:
        return None

    return result[0]

def get_sleep_id(user_id):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id FROM sleep_records
            WHERE user_id = ? AND wake_time IS NOT NULL
            ORDER BY id DESC
            LIMIT 1
            """,
            (user_id,)
        )
        result = cursor.fetchone()

    if result is None:
        return None

    return result[0]

def save_wake_time(user_id, wake_time):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
        """
        UPDATE sleep_records
        SET wake_time = ?
        WHERE user_id = ? AND wake_time IS NULL
        """,
        (wake_time, user_id)
        )

def save_sleep_quality(user_id, quality_score):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
        """
        UPDATE sleep_records
        SET sleep_quality = ?
        WHERE id = (
            SELECT id FROM sleep_records
            WHERE user_id = ? AND sleep_quality IS NULL
            ORDER BY id DESC
            LIMIT 1
        )
        """,
        (quality_score, user_id)
        )

def save_notes(text, sleep_record_id):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO notes (text, sleep_record_id) 
            VALUES (?, ?);
            """,
            (text, sleep_record_id)
        )


def all_notes(sleep_record_id):
    with connect("sleep_bot.db") as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT text FROM notes
            WHERE sleep_record_id = ?
            """,
            (sleep_record_id,)
        )
        texts = cursor.fetchall()
    return [text for (text,) in texts]

bot.polling(non_stop=True, interval=0)