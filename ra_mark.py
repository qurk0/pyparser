from datetime import datetime

from ra_version import insert_ra_version

def get_student_id(conn, student_name):
    """
    Получает student_id из таблицы students по имени студента.
    Работает как со студентами с полным ФИО (Фамилия И.А.), так и без отчества (Фамилия И.).
    """
    with conn.cursor() as cursor:
        # Разделяем инициалы на фамилию и инициалы имени и отчества
        parts = student_name.split()
        if len(parts) != 2:
            raise ValueError(
                f"Некорректный формат имени студента: {student_name}"
            )
        surname = parts[0]
        initials = parts[1]
        # Проверяем, есть ли отчество в инициалах
        if "." in initials and len(initials.split(".")) == 3:
            query = """
                SELECT id
                FROM students
                WHERE middle_name = %s
                  AND CONCAT(LEFT(first_name, 1), '.', LEFT(last_name, 1), '.') = %s
            """
            cursor.execute(query, (surname, initials))
        else:  # Без отчества: И.
            query = """
                SELECT id
                FROM students
                WHERE middle_name = %s
                  AND CONCAT(LEFT(first_name, 1), '.') = %s
                  AND (last_name IS NULL OR last_name = '')
            """
            cursor.execute(query, (surname, initials))
        result = cursor.fetchone()
        if result is None:
            return None            
        return result[0]
    
def insert_ra_mark(conn, students, control_ids):
    version_comment = f"Добавление оценок студентов от {datetime.now()}"

    version_id = insert_ra_version(
        conn,
        version_comment,
    )

    with conn.cursor() as cursor:
        query = """
            INSERT INTO ra_mark (
                version_id,
                stud_id,
                control_id,
                grade
            )
            VALUES (%s, %s, %s, %s)
        """

        for student in students:
            student_id = get_student_id(
                conn,
                student.name,
            )

            if student_id is None:
                raise ValueError(
                    f"Студент '{student.name}' "
                    f"не найден в таблице students"
                )

            for grade in student.grades:
                discipline_title = grade.control.discipline.title

                key = (
                    discipline_title,
                    grade.control.control_type,
                )

                control_id = control_ids.get(key)

                if control_id is None:
                    raise ValueError(
                        f"Не найден control_id для дисциплины "
                        f"'{discipline_title}' с формой "
                        f"'{grade.control.control_type}'"
                    )

                cursor.execute(
                    query,
                    (
                        version_id,
                        student_id,
                        control_id,
                        grade.value,
                    ),
                )

    print("[+] Таблица ra_mark успешно заполнена.")
    return version_id