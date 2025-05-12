from datetime import timedelta, datetime

import psycopg2
import os

# Конфигурация подключения к PostgreSQL
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),  # Имя базы данных
    "user": os.getenv("DB_USER"),  # Имя пользователя
    "password": os.getenv("DB_PASSWORD"),  # Пароль
    "host": os.getenv("DB_HOST"),  # Хост (имя сервиса)
    "port": os.getenv("DB_PORT", "5432")  # Порт (по умолчанию 5432)
}

# Функция для инициализации базы данных
def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Проверяем, существует ли таблица users
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'users'
        );
    """)
    if not cursor.fetchone()[0]:
        # Если таблица не существует, создаем её
        cursor.execute("""
            CREATE TABLE users (
                user_id BIGINT PRIMARY KEY,
                username TEXT,
                subscription_status TEXT DEFAULT 'inactive',
                subscription_end_date DATE,
                reminder_sent BOOLEAN DEFAULT FALSE
            );
        """)

    # Проверяем, существует ли таблица transactions
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'transactions'
        );
    """)
    if not cursor.fetchone()[0]:
        # Если таблица не существует, создаем её
        cursor.execute("""
            CREATE TABLE transactions (
                tx_hash TEXT PRIMARY KEY,
                user_id BIGINT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)


    # Проверяем, существует ли таблица promo_codes
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'promo_codes'
        );
    """)
    if not cursor.fetchone()[0]:
        # Если таблица не существует, создаем её
        cursor.execute("""
            CREATE TABLE promo_codes (
            code TEXT PRIMARY KEY,
            days INTEGER NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            used_by BIGINT
            );
        """)

    conn.commit()
    conn.close()

# Функция для добавления пользователя в базу данных
def add_user(user_id, username):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """, (user_id, username))
    conn.commit()
    conn.close()

# Функция для обновления статуса подписки
def update_subscription(user_id, status, end_date):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET subscription_status = %s, subscription_end_date = %s, reminder_sent = FALSE
        WHERE user_id = %s;
    """, (status, end_date, user_id))
    conn.commit()
    conn.close()

# Функция для получения всех активных пользователей
def get_active_users():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, subscription_end_date
        FROM users
        WHERE subscription_status = 'active';
    """)
    users = cursor.fetchall()
    conn.close()
    return users

# Функция для получения статуса подписки
def get_subscription_status(user_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subscription_status, subscription_end_date, reminder_sent
        FROM users
        WHERE user_id = %s;
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        subscription_status, subscription_end_date, reminder_sent = result
        # Преобразуем дату в строку, если она существует
        subscription_end_date = subscription_end_date.strftime("%Y-%m-%d") if subscription_end_date else None
        return subscription_status, subscription_end_date, reminder_sent
    return "inactive", None, False

# Функция для проверки, был ли хэш транзакции уже использован
def is_transaction_used(tx_hash):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tx_hash FROM transactions WHERE tx_hash = %s;
    """, (tx_hash,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для сохранения успешной транзакции
def save_transaction(tx_hash, user_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (tx_hash, user_id)
        VALUES (%s, %s)
        ON CONFLICT (tx_hash) DO NOTHING;
    """, (tx_hash, user_id))
    conn.commit()
    conn.close()

# Функция для обновления флага напоминания
def set_reminder_sent(user_id, sent=True):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET reminder_sent = %s
        WHERE user_id = %s;
    """, (sent, user_id))
    conn.commit()
    conn.close()


# Функция для проверки существования промокода
def check_promo_code(code):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT days, used FROM promo_codes WHERE code = %s;
    """, (code,))
    result = cursor.fetchone()
    conn.close()
    return result  # Возвращает кортеж (days, used) или None

# Функция для пометки промокода как использованного
def mark_promo_code_as_used(code, user_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE promo_codes
        SET used = TRUE, used_by = %s
        WHERE code = %s;
    """, (user_id, code))
    conn.commit()
    conn.close()

# Функция для обновления подписки пользователя с учетом промокода
def update_subscription_with_promo(user_id, days_to_add):
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subscription_status, subscription_end_date FROM users WHERE user_id = %s;
    """, (user_id,))
    result = cursor.fetchone()

    if result:
        subscription_status, subscription_end_date = result

        # Проверяем, является ли subscription_end_date строкой или None
        if subscription_end_date:
            if isinstance(subscription_end_date, str):
                # Если строка, преобразуем в datetime.date
                current_end_date = datetime.strptime(subscription_end_date, "%Y-%m-%d").date()
            else:
                # Если уже datetime.date, используем как есть
                current_end_date = subscription_end_date
        else:
            # Если подписка неактивна, устанавливаем текущую дату
            current_end_date = datetime.now().date()

        # Рассчитываем новую дату окончания подписки
        new_end_date = (current_end_date + timedelta(days=days_to_add)).strftime("%Y-%m-%d")

        # Обновляем статус подписки
        cursor.execute("""
            UPDATE users
            SET subscription_status = 'active', subscription_end_date = %s
            WHERE user_id = %s;
        """, (new_end_date, user_id))
    conn.commit()
    conn.close()