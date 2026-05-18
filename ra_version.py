from datetime import datetime

def insert_ra_version(conn, comment):
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO ra_version (created, comment)
                VALUES (%s, %s)
                RETURNING id
            """
            current_time = datetime.now()
            cursor.execute(query, (current_time, comment))
            version_id = cursor.fetchone()[0]
            conn.commit()
            return version_id
    except Exception as e:
        print(f"[!] Ошибка при создании версии: {e}")
        conn.rollback()
        return None

