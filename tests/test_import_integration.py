import os
from copy import deepcopy
from pathlib import Path

import psycopg2
import pytest
from dotenv import load_dotenv

from html_parser import parse_html
from main import import_report
from ra_mark import get_student_id
from ra_results import collect_ra_results

FIXTURES_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture
def get_conn():
    load_dotenv()

    DB_CONFIG = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }

    conn = psycopg2.connect(
        **DB_CONFIG,
        connect_timeout=5,
    )

    yield conn

    conn.rollback()
    conn.close()

def get_count(conn, table_name):
    with conn.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]

def test_import_report_success(get_conn):
    report = parse_html(FIXTURES_DIR / "test.html")

    versions_before = get_count(
        get_conn,
        "ra_version",
    )

    marks_before = get_count(
        get_conn,
        "ra_mark",
    )

    import_report(
        get_conn,
        report,
    )

    versions_after = get_count(
        get_conn,
        "ra_version",
    )

    marks_after = get_count(
        get_conn,
        "ra_mark",
    )

    expected_marks = sum(
        len(student.grades)
        for student in report.students
    )

    expected_students = len(report.students)

    # Получаем version_id, созданный текущим импортом.
    with get_conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM ra_version
            ORDER BY id DESC
            LIMIT 1
            """
        )
        version_id = cur.fetchone()[0]

        cur.execute(
            """
            SELECT COUNT(DISTINCT stud_id)
            FROM ra_mark
            WHERE version_id = %s
            """,
            (version_id,),
        )
        actual_students = cur.fetchone()[0]

    assert versions_after == versions_before + 1
    assert marks_after == marks_before + expected_marks
    assert actual_students == expected_students

def test_import_report_rollback(get_conn):
    report = parse_html(FIXTURES_DIR / "test_rollback.html")

    versions_before = get_count(
        get_conn,
        "ra_version",
    )

    marks_before = get_count(
        get_conn,
        "ra_mark",
    )

    report.students[1].name = "Несуществующая Д.Х."

    with pytest.raises(
        ValueError,
        match="не найден в таблице students",
    ):
        import_report(
            get_conn,
            report,
        )

    # В текущей транзакции часть данных уже успела вставиться.
    versions_during_transaction = get_count(
        get_conn,
        "ra_version",
    )

    marks_during_transaction = get_count(
        get_conn,
        "ra_mark",
    )

    assert versions_during_transaction == versions_before + 1
    assert marks_during_transaction > marks_before

    # Именно это делает main() при ошибке.
    get_conn.rollback()

    versions_after_rollback = get_count(
        get_conn,
        "ra_version",
    )

    marks_after_rollback = get_count(
        get_conn,
        "ra_mark",
    )

    assert versions_after_rollback == versions_before
    assert marks_after_rollback == marks_before

def test_collect_ra_results_only_contains_students_from_current_version(get_conn):
    conn = get_conn

    report = parse_html(FIXTURES_DIR / "test.html")

    import_report(
        conn,
        report,
    )

    with conn.cursor() as cur:
        # Берём существующего студента.
        cur.execute("SELECT id FROM students LIMIT 1")
        student_with_marks = cur.fetchone()[0]

        # Создаём отдельную тестовую версию.
        cur.execute(
            """
            INSERT INTO ra_version (created, comment)
            VALUES (NOW(), 'collect_ra_results test')
            RETURNING id
            """
        )
        version_id = cur.fetchone()[0]

        # После обычного импорта формы контроля уже существуют.
        cur.execute("SELECT id FROM ra_control LIMIT 1")
        control_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO ra_mark (
                version_id,
                stud_id,
                control_id,
                grade
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                version_id,
                student_with_marks,
                control_id,
                5,
            ),
        )

    results = collect_ra_results(
        conn=conn,
        sem=1,
        version_id=version_id,
    )

    student_ids = [
        result["stud_id"]
        for result in results
    ]

    assert student_ids == [student_with_marks]

def test_retake_changes_student_rating(get_conn):
    report = parse_html(FIXTURES_DIR / "test.html")

    # Первая версия — исходные результаты.
    import_report(
        get_conn,
        report,
    )

    # Берём студента с последнего места рейтинга.
    with get_conn.cursor() as cur:
        cur.execute(
            """
            SELECT stud_id, position, total_score, percent
            FROM ra_results
            ORDER BY position DESC
            LIMIT 1
            """
        )
        before = cur.fetchone()

    stud_id, position_before, score_before, percent_before = before

    # Находим этого студента в ParsedReport.
    report_after_retake = deepcopy(report)

    student = next(
        student
        for student in report_after_retake.students
        if get_student_id(get_conn, student.name) == stud_id
    )

    # Имитируем максимально успешную пересдачу:
    # все оценки студента делаем максимальными для
    # соответствующей формы контроля.
    for grade in student.grades:
        max_grade = {
            1: -3,  # зачёт
            2: 5,
            3: 5,
            4: 5,
        }[grade.control.control_type]

        grade.value = max_grade

    results_count_before = get_count(get_conn, "ra_results")

    # Вторая версия — полный снимок после пересдачи.
    import_report(
        get_conn,
        report_after_retake,
    )

    results_count_after = get_count(get_conn, "ra_results")

    assert results_count_after == results_count_before

    with get_conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT stud_id, COUNT(*)
            FROM ra_results
            GROUP BY stud_id
            HAVING COUNT(*) > 1
            """
        )
        duplicates = cursor.fetchall()

    assert duplicates == []

    with get_conn.cursor() as cur:
        cur.execute(
            """
            SELECT position, total_score, percent, diff_score, diff_percent
            FROM ra_results
            WHERE stud_id = %s
            """,
            (stud_id,),
        )
        after = cur.fetchone()

    (
        position_after,
        score_after,
        percent_after,
        diff_score,
        diff_percent,
    ) = after

    assert score_after >= score_before
    assert percent_after >= percent_before

    assert diff_score == score_after - score_before
    assert diff_percent == round(percent_after - percent_before, 2)

    assert position_after < position_before