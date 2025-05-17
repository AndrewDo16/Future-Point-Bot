from perisist.database import get_connection


def get_primary_wallet():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT wallet, chain FROM telegram.crypto_wallet WHERE is_primary = true;
    """)
    result = cursor.fetchone()
    conn.close()
    if result:
        wallet, crypto = result
        return wallet, crypto
    return None