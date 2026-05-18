import os
import sys
import psycopg2
import re

from dotenv import load_dotenv
from datetime import datetime

from html_parser import parse_html
from csv_parser import parse_csv

from ra_disc import get_disc_id_by_title

from ra_plan import get_plan_for_group, fill_new_plan

from ra_control import get_control_id_by_disc_plan_form_sem, fill_ra_control

from ra_mark import insert_ra_mark

from ra_results import insert_ra_results


load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
print(DB_CONFIG)


def get_current_semester(group_name):
    # Извлечение года поступления (последние две цифры)
    match = re.search(r'\d{2}$', group_name)
    if not match:
        return "Ошибка при извлечении года"
    admission_year = 2000 + int(match.group())

    # Текущая дата
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.month

    # Вычисление курса
    years_passed = current_year - admission_year
    if current_month >= 9:
        course = years_passed + 1
    else:
        course = years_passed

    # Вычисление семестра
    if 2 <= current_month <= 8:
        semester = course * 2  # Летний
    else:
        semester = course * 2 - 1  # Зимний

    return semester

def main():
    if len(sys.argv) != 2:
        print("Использование программы: make load file=Имя_файла.html ИЛИ file=Имя_файла.csv")
        sys.exit(1)
    
    filename = sys.argv[1]
    ext = os.path.splitext(filename)[1].lower()

    conn = psycopg2.connect(**DB_CONFIG, connect_timeout=5)

    try:
        if ext == ".html":
            group_name, disciplines, students = parse_html(filename)
        elif ext == ".csv":
            group_name, disciplines, students = parse_csv(filename)
        else:
            print(f"[!] Неподдерживаемое расширение файла: {ext}")
            sys.exit(1)

        semester = get_current_semester(group_name)
        plan_id = get_plan_for_group(conn, group_name)
        if plan_id == None:
            plan_id = fill_new_plan(conn, group_name)
                
        disc_ids = {}
        for disc in disciplines:
            disc_ids[disc["title"]] = get_disc_id_by_title(connection=conn, title=disc["title"])
            if disc_ids[disc["title"]] == None:
                print(f"[!] Ошибка: отсутствует информация о предмете: {disc["title"]}")
                sys.exit(1)
        
        non_control_id_discs = []
        for disc in disciplines:
            control_id = get_control_id_by_disc_plan_form_sem(
                    connection=conn, 
                    plan_id=plan_id,
                    disc_id=disc_ids[disc["title"]],
                    form=disc["type"],
                    sem=semester
                )
            # Так как у одной дисциплины может быть несколько типов аккредитации, 
            # то уникальным ключом будет являться результат 
            # конкатенации названия предмета и типа аккредитации
            if control_id == None:
                non_control_id_discs.append(disc)
        if len(non_control_id_discs) != 0:
            fill_ra_control(
                            connection=conn, 
                            plan_id=plan_id, 
                            semester=semester, 
                            disciplines=non_control_id_discs
                        )

        insert_ra_mark(conn=conn, students=students, plan_id=plan_id, sem=semester)

        insert_ra_results(conn=conn, sem=semester)
        print(f"[+] Данные из файла {filename} успешно занесены!")
    except Exception as e:
        print(f"[!] При выполнении программы произошла ошибка: {e}")
        sys.exit(1)
    finally:
        conn.close()
        
        

        # Порядок заполнения БД:
        # 1) Парсим данные. Они прилетают в виде трёх структур: 
        #    - group_name    - названи
        #    - disciplines   - список дисциплин, где дисциплина - словарь
        #    - - ["title"]   - ключ, по которому получаем название предмета
        #    - - ["type"]    - ключ, по которому получаем тип аккредитации (нормализованный в соотв. с TYPE_MAPPING в normalization.py)
        #    - students      - список студентов, где студент - словарь
        #    - - ["id"]      - ключ, по которому получаем студенческий шифр студента
        #    - - ["name"]    - ключ, по которому получаем полные ФИО студента
        #    - - ["grades"]  - ключ, по которому получаем список словарей с оценками ["discipline" - название предмета, "type" - тип аккредитации, "grade" - оценка]
        # 2) Определяем текущий семестр у группы, оценки которой пришли в программу
        # 3) Проверяем наличие плана для группы студентов (план на каждый курс уникален, каждое новое поступление - новый план, проверяем год поступления по первым двум числам в названии группы)
        # 4) Проверяем наличие дисциплин в таблице ra_disc
        # 5) Проверяем таблицу ra_control на наличие в ней записей о нынешних дисциплинах и типах аккредитации для конкретного семестра. Если чего-то нет - создаём
        # 6) Заполняем таблицу ra_mark
        # 7) Заполняем таблицу ra_results

if __name__ == "__main__":
    main()