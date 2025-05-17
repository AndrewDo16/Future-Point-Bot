from datetime import timedelta, datetime
from perisist.database import get_connection

# Функция для добавления пользователя в базу данных
def add_user(user_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO telegram.users (user_id, username)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO NOTHING;
    """, (user_id, username))
    conn.commit()
    conn.close()

# Функция для обновления статуса подписки
def update_subscription(user_id, status, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE telegram.users
        SET subscription_status = %s, subscription_end_date = %s
        WHERE user_id = %s;
    """, (status, end_date, user_id))
    conn.commit()
    conn.close()

# Функция для получения всех активных пользователей
def get_active_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, subscription_end_date
        FROM telegram.users
        WHERE subscription_status = 'active';
    """)
    users = cursor.fetchall()
    conn.close()
    return users

# Функция для получения всех активных пользователей
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_id, subscription_end_date
        FROM telegram.users;
    """)
    users = cursor.fetchall()
    conn.close()
    return users

# Функция для получения статуса подписки
def get_subscription_status(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subscription_status, subscription_end_date
        FROM telegram.users
        WHERE user_id = %s;
    """, (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        subscription_status, subscription_end_date = result
        # Преобразуем дату в строку, если она существует
        subscription_end_date = subscription_end_date.strftime("%Y-%m-%d") if subscription_end_date else None
        return subscription_status, subscription_end_date
    return "inactive", None


# Функция для обновления подписки пользователя с учетом промокода
def update_subscription_with_promo(user_id, days_to_add):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT subscription_status, subscription_end_date
                   FROM telegram.users
                   WHERE user_id = %s;
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
                       UPDATE telegram.users
                       SET subscription_status   = 'active',
                           subscription_end_date = %s
                       WHERE user_id = %s;
                       """, (new_end_date, user_id))
    conn.commit()
    conn.close()