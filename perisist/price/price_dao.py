from perisist.database import get_connection


def get_price_for_usdt_by_period(period):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT price FROM telegram.price WHERE currency = 'USDT' AND subscription_period_month = %s
    """, (period,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_total_day_for_usdt(period):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subscription_period_days FROM telegram.price WHERE currency = 'RUB' AND subscription_period_month = %s
    """, (period,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_price_for_rub_by_period(period):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT price FROM telegram.price WHERE currency = 'RUB' AND subscription_period_month = %s
    """, (period,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_total_day_for_rub(period):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subscription_period_days FROM telegram.price WHERE currency = 'RUB' AND subscription_period_month = %s
    """, (period,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None