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

def get_current_semester(group_name):
    # Извлечение года поступления (последние две цифры)
    match = re.search(r'\d{2}$', group_name)
    if not match:
        raise ValueError(
            f"Не удалось определить год поступления из группы '{group_name}'"
        )
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

def import_report(conn, report):
    group_name = report.group_name
    controls = report.controls
    students = report.students
    semester = get_current_semester(group_name)
    plan_id = get_plan_for_group(
        conn,
        group_name,
    )
    if plan_id is None:
        plan_id = fill_new_plan(
            conn,
            group_name,
        )
    disc_ids = {}
    for control in controls:
        title = control.discipline.title
        disc_id = get_disc_id_by_title(
            connection=conn,
            title=title,
        )
        if disc_id is None:
            raise ValueError(
                f"Отсутствует информация о предмете: {title}"
            )
        disc_ids[title] = disc_id
    missing_controls = []
    for control in controls:
        title = control.discipline.title
        control_id = get_control_id_by_disc_plan_form_sem(
            connection=conn,
            plan_id=plan_id,
            disc_id=disc_ids[title],
            form=control.control_type,
            sem=semester,
        )
        if control_id is None:
            missing_controls.append(control)
    if missing_controls:
        fill_ra_control(
            connection=conn,
            plan_id=plan_id,
            semester=semester,
            controls=missing_controls,
        )

    control_ids = {}

    for control in controls:
        title = control.discipline.title

        control_id = get_control_id_by_disc_plan_form_sem(
            connection=conn,
            plan_id=plan_id,
            disc_id=disc_ids[title],
            form=control.control_type,
            sem=semester,
        )

        if control_id is None:
            raise ValueError(
                f"Не найден control_id для дисциплины "
                f"'{title}' с формой '{control.control_type}'"
            )

        control_ids[(title, control.control_type)] = control_id
    version_id = insert_ra_mark(
        conn=conn,
        students=students,
        control_ids=control_ids,
    )
    insert_ra_results(
        conn=conn,
        sem=semester,
        version_id=version_id,
    )

def main():
    if len(sys.argv) != 2:
        print(
            "Использование программы: "
            "make load file=Имя_файла.html "
            "ИЛИ file=Имя_файла.csv"
        )
        sys.exit(1)

    filename = sys.argv[1]
    ext = os.path.splitext(filename)[1].lower()

    conn = None

    try:
        if ext == ".html":
            report = parse_html(filename)
        elif ext == ".csv":
            report = parse_csv(filename)
        else:
            raise ValueError(
                f"Неподдерживаемое расширение файла: {ext}"
            )

        conn = psycopg2.connect(
            **DB_CONFIG,
            connect_timeout=5,
        )

        import_report(
            conn,
            report,
        )

        conn.commit()

        print(
            f"[+] Данные из файла {filename} "
            f"успешно занесены!"
        )

    except Exception as e:
        if conn is not None:
            conn.rollback()

        print(
            f"[!] При выполнении программы "
            f"произошла ошибка: {e}"
        )

        sys.exit(1)

    finally:
        if conn is not None:
            conn.close()        
        
if __name__ == "__main__":
    main()