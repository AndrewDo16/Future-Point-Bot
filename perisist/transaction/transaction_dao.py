from perisist.database import get_connection


# Функция для проверки, был ли хэш транзакции уже использован
def is_transaction_used(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT transaction_id FROM telegram.transactions WHERE transaction_id = %s;
    """, (transaction_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Функция для сохранения успешной транзакции
def save_transaction(transaction_id, total_price, currency, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO telegram.transactions (transaction_id, total_amount, currency, user_id)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (transaction_id) DO NOTHING;
    """, (transaction_id, total_price, currency, user_id))
    conn.commit()
    conn.close()