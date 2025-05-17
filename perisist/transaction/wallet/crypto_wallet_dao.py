from perisist.database import get_connection


def get_wallet_for_usdt():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT wallet, chain FROM telegram.crypto_wallet;
    """)
    result = cursor.fetchone()
    conn.close()
    if result:
        wallet, crypto = result
        return wallet, crypto
    return None