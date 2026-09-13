from datetime import datetime

def insert_ra_version(conn, comment):
    with conn.cursor() as cursor:
        query = """
            INSERT INTO ra_version (created, comment)
            VALUES (%s, %s)
            RETURNING id
        """
        current_time = datetime.now()
        cursor.execute(
            query,
            (
                current_time,
                comment,
            ),
        )
        version_id = cursor.fetchone()[0]
        return version_id