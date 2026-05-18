from datetime import datetime
from ra_version import insert_ra_version
from ra_plan import parse_group_info
from ra_control import get_control_id_by_disc_plan_form_sem

def get_student_id(conn, student_name):
    """
    Получает student_id из таблицы students по имени студента.
    Работает как со студентами с полным ФИО (Фамилия И.А.), так и без отчества (Фамилия И.).
    """
    try:
        with conn.cursor() as cursor:
            # Разделяем инициалы на фамилию и инициалы имени и отчества
            parts = student_name.split(" ")
            if len(parts) != 2:
                print(f"[!] Некорректный формат имени студента: {student_name}")
                return None

            middle_name = parts[0]
            initials = parts[1]

            # Проверяем, есть ли отчество в инициалах
            if "." in initials and len(initials.split(".")) == 3:
                query = """
                    SELECT id
                    FROM students
                    WHERE middle_name = %s
                      AND CONCAT(LEFT(first_name, 1), '.', LEFT(last_name, 1), '.') = %s
                """
                cursor.execute(query, (middle_name, initials))
            else:  # Без отчества: И.
                query = """
                    SELECT id
                    FROM students
                    WHERE middle_name = %s
                      AND CONCAT(LEFT(first_name, 1), '.') = %s
                      AND (last_name IS NULL OR last_name = '')
                """
                cursor.execute(query, (middle_name, initials))

            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"[!] Ошибка при получении student_id: {e}")
        return None

def get_disc_id(conn, discipline_name):
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT id
                FROM ra_disc
                WHERE title = %s
            """
            cursor.execute(query, (discipline_name,))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"[!] Ошибка при получении disc_id: {e}")
        return None
    
def get_plan_id(conn, group_name):
    try:
        with conn.cursor() as cursor:
            query = '''
                SELECT id
                FROM ra_plan
                WHERE year = %s AND level = %s;
            '''

            data = parse_group_info(group_name)
            cursor.execute(query, (data["year"], data["level"]))
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception as e:
        print(f"[!] Ошибка при получении control_id: {e}")
        return None

def insert_ra_mark(conn, students, plan_id, sem):
    try:
        # Создаём новую версию в ra_version
        version_comment = f"Добавление оценок студентов от {datetime.now()}"
        version_id = insert_ra_version(conn, version_comment)
        if not version_id:
            print("[!] Не удалось создать запись в ra_version.")
            return

        with conn.cursor() as cursor:
            query = """
                INSERT INTO ra_mark (version_id, stud_id, control_id, grade)
                VALUES (%s, %s, %s, %s)
            """

            for student in students:
                student_id = get_student_id(conn, student["name"])
                if not student_id:
                    print(f"[!] Студент '{student["name"]}' не найден в таблице students.")
                    return

                for grade_info in student["grades"]:
                    # Получаем disc_id
                    disc_id = get_disc_id(conn, grade_info["discipline"])
                    if not disc_id:
                        print(f"[!] Дисциплина '{grade_info["discipline"]}' не найдена в таблице ra_disc.")
                        return

                    # Получаем control_id
                    control_id = get_control_id_by_disc_plan_form_sem(conn, disc_id=disc_id, plan_id=plan_id, form=grade_info["type"], sem=sem)
                    if not control_id:
                        print(f"[!] Не найден control_id для дисциплины '{grade_info["discipline"]}' с формой '{grade_info["type"]}'.")
                        return

                    # Вставляем запись в ra_mark
                    cursor.execute(query, (version_id, student_id, control_id, grade_info["grade"]))

            conn.commit()
            print("[+] Таблица ra_mark успешно заполнена.")
    except Exception as e:
        print(f"[!] Ошибка при заполнении таблицы ra_mark: {e}")
        conn.rollback()
