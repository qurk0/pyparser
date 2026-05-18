from dotenv import load_dotenv
import os
import psycopg2
import sys

load_dotenv()
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
deps_list = '''Введите, к какой кафедре относится предмет:
1 - предмет кафедры Вега
2 - предмет кафедры Высшей Математики
3 - предмет кафедры Вега
4 - предмет кафедры Высшей Математики
5 - предмет другой кафедры
'''

def connect_to_db():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        print("[+] Подключение к БД установлено!")
        return connection
    except Exception as e:
        print(f"[!] Ошибка подключения к БД : {e}")
        sys.exit(1)
    
def close_connection(connection):
    if connection:
        connection.close()
        print("[!] Соединение с БД успешно закрыто!")

def get_data_to_fill():
    data = {}
    data["title"] = input("Введите полное название предмета: ")
    data["shorttitle"] = input("Введите сокращенное название предмета: ")
    data["departament_id"] = input(deps_list + ": ")
    
    return data

def pull_data_to_db(connection, data):
    try:
        cursor = connection.cursor()

        insert_query = '''
        INSERT INTO ra_disc (title, shorttitle, department_id)
        VALUES (%s, %s, %s)
        RETURNING id
        '''

        cursor.execute(insert_query, (data["title"], data["shorttitle"], data["departament_id"]))
        inserted_id = cursor.fetchone()[0]
        connection.commit()

        print(f"[+] Данные о дисциплине {data["shorttitle"]} успешно добавлены в ra_disc с id: {inserted_id}")
        return inserted_id
    except Exception as e:
        print(f"[!] Ошибка при внесении данных в таблицу : {e}")
        connection.rollback()
        return None
    finally: 
        cursor.close()

def get_disc_id_by_title(connection, title):
    try:
        cursor = connection.cursor()

        # SQL-запрос для получения disc_id
        select_query = '''
        SELECT id FROM ra_disc
        WHERE title = %s;
        '''
        cursor.execute(select_query, (title,))
        result = cursor.fetchone()

        if result:
            disc_id = result[0]
            print(f"[+] Найден предмет '{title}' с id: {disc_id}")
            return disc_id
        else:
            print(f"[!] Предмет '{title}' не найден в таблице ra_disc.")
            return None
    except Exception as e:
        print(f"[!] Ошибка при выполнении запроса: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()

def get_dep_by_id(connection, disc_id):
    try:
        cursor = connection.cursor()

        select_query = '''
        SELECT departament_id FROM ra_disc
        WHERE id = %s;
        '''
        cursor.execute(select_query, (disc_id,))
        result = cursor.fetchone()

        if result:
            dep_id = result[0]
            (f"[+] Предмет с id {disc_id}' принадлежит {dep_id} кафедре")
            return dep_id
        else:
            print(f"[!] Предмет с id = '{disc_id}' не найден в таблице ra_disc.")
            return None
    except Exception as e:
        print(f"[!] Ошибка при выполнении запроса: {e}")
        return None
    finally:
        if 'cursor' in locals():
            cursor.close()

if __name__ == "__main__":
    con = connect_to_db()
    print("\n[!] Программа будет работать до остановки пользователем. \nДля остановки нажмите Ctrl+C.\n")
    try:
        while True:
            pull_data_to_db(con, get_data_to_fill())
    except KeyboardInterrupt:
        print("\n[!] Программа остановлена пользователем.")
    finally:
        close_connection(con)