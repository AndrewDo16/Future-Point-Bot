# Вызов группы по имени

from perisist.database import get_connection

def get_chat_id_by_group_name(group_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT chat_id FROM telegram.groups WHERE group_name = %s;
    """, (group_name,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_all_group():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT chat_id FROM telegram.groups
    """)
    all_groups = [row[0] for row in cursor.fetchall()]
    conn.close()
    return all_groups