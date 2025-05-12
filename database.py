import sqlite3

# Функция для инициализации базы данных
def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    # Проверяем, существует ли таблица users
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='users'
    ''')
    if not cursor.fetchone():
        # Если таблица не существует, создаем её
        cursor.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                subscription_status TEXT DEFAULT 'inactive',
                subscription_end_date TEXT,
                reminder_sent BOOLEAN DEFAULT FALSE
            )
        ''')

    # Проверяем, существует ли таблица transactions
    cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'
    ''')
    if not cursor.fetchone():
        # Если таблица не существует, создаем её
        cursor.execute('''
            CREATE TABLE transactions (
                tx_hash TEXT PRIMARY KEY,
                user_id INTEGER,
                timestamp TEXT
            )
        ''')
    conn.commit()
    conn.close()

# Функция для добавления пользователя в базу данных
def add_user(user_id, username):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username)
        VALUES (?, ?)
    ''', (user_id, username))
    conn.commit()
    conn.close()

# Функция для обновления статуса подписки
def update_subscription(user_id, status, end_date):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET subscription_status = ?, subscription_end_date = ?, reminder_sent = FALSE
        WHERE user_id = ?
    ''', (status, end_date, user_id))
    conn.commit()
    conn.close()

# Функция для получения статуса подписки
def get_subscription_status(user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT subscription_status, subscription_end_date, reminder_sent FROM users
        WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0], result[1], result[2]  # Возвращаем статус, дату окончания и флаг напоминания
    return "inactive", None, False

# Функция для обновления флага напоминания
def set_reminder_sent(user_id, sent=True):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users
        SET reminder_sent = ?
        WHERE user_id = ?
    ''', (sent, user_id))
    conn.commit()
    conn.close()

# Функция для проверки, был ли хэш транзакции уже использован
def is_transaction_used(tx_hash):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT tx_hash FROM transactions WHERE tx_hash = ?
    ''', (tx_hash,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для сохранения успешной транзакции
def save_transaction(tx_hash, user_id):
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (tx_hash, user_id, timestamp)
        VALUES (?, ?, datetime('now'))
    ''', (tx_hash, user_id))
    conn.commit()
    conn.close()

# Функция для получения всех пользователей
def get_all_users():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT user_id FROM users
    ''')
    users = cursor.fetchall()
    conn.close()
    return users