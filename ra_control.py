from ra_disc import get_disc_id_by_title
import normalization as n

def fill_ra_control(connection, plan_id, semester, disciplines):
    try:
        cursor = connection.cursor()
        
        for discipline in disciplines:
            disc_id = get_disc_id_by_title(connection, discipline["title"])
            max_grade = n.TYPE_GRADE_MAPPING.get(discipline["type"], None)
            insert_query = '''
            INSERT INTO ra_control (plan_id, disc_id, sem, form, max_grade)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            '''
            cursor.execute(insert_query, (plan_id, disc_id, semester, discipline["type"], max_grade))
            inserted_id = cursor.fetchone()[0]
            connection.commit()

            print(f"[+] Данные успешно добавлены в ra_control с id: {inserted_id}!")

    except Exception as e:
        print(f"[!] Ошибка при заполнении таблицы ra_control: {e}!")
        connection.rollback()
    finally:
        cursor.close()

def get_control_id_by_disc_plan_form_sem(connection, plan_id, disc_id, form, sem):
    """
    Параметры:
    connection - соединение с БД
    plan_id - ID учебного плана
    disc_id - ID дисциплины
    form - форма аккредитации (или тип аккредитации, как угодно можно обозвать)
    sem - семестр когда дисциплина сдаётся
    """
    try:
        with connection.cursor() as cursor:
            # SQL-запрос для получения control_id
            query = """
                SELECT id
                FROM ra_control
                WHERE disc_id = %s AND form = %s AND plan_id = %s AND sem = %s
            """
            cursor.execute(query, (disc_id, form, plan_id, sem))
            result = cursor.fetchone()
            if result:
                return result[0]  # Возвращаем control_id
            else:
                return None
    except Exception as e:
        print(f"[!] Ошибка при получении control_id: {e}")
        return None
