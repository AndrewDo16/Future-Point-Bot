# Функция для проверки существования промокода
from perisist.database import get_connection


def check_promo_code(code):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT days, used FROM telegram.promo_codes WHERE code = %s;
    """, (code,))
    result = cursor.fetchone()
    conn.close()
    return result  # Возвращает кортеж (days, used) или None

# Функция для пометки промокода как использованного
def mark_promo_code_as_used(code, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE telegram.promo_codes
        SET used = TRUE, used_by = %s
        WHERE code = %s;
    """, (user_id, code))
    conn.commit()
    conn.close()