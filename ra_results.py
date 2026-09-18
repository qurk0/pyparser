from collections import defaultdict


def get_marks_with_context(conn, version_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                rm.stud_id,
                rc.sem,
                rc.form,
                rc.max_grade,
                rd.department_id,
                rm.grade
            FROM ra_mark rm
            JOIN ra_control rc ON rm.control_id = rc.id
            JOIN ra_disc rd ON rc.disc_id = rd.id
            WHERE rm.version_id = %s
            """,
            (version_id,),
        )

        rows = cur.fetchall()

    return [
        {
            "stud_id": row[0],
            "sem": row[1],
            "form": row[2],
            "max_grade": row[3],
            "department_id": row[4],
            "grade": row[5],
        }
        for row in rows
    ]


def calculate_scores_and_departments_with_percent(marks_with_context):
    """
    Вычисляет и возвращает:
    - session_score
    - total_score
    - баллы за предметы веги
    - баллы за предметы кафедры вм
    - баллы за предметы других кафедр
    - percent (в процентах от максимально возможного)
    """
    

    scores_by_sem = defaultdict(int)
    vega = vm = other = 0
    max_possible_score = 0

    for mark in marks_with_context:
        grade = mark["grade"]
        sem = mark["sem"]
        department_id = mark["department_id"]
        max_grade = mark["max_grade"]

        if grade is None or grade in (0, -7, -8, -9):
            continue

        # Учитываем только то, что реально сдано
        if grade == -3:
            grade = abs(grade)

        if max_grade == -3:
            max_grade = abs(max_grade)

        scores_by_sem[sem] += grade
        max_possible_score += max_grade

        if department_id in (1, 3):
            vega += grade
        elif department_id in (2, 4):
            vm += grade
        elif department_id == 5:
            other += grade

    if not scores_by_sem or max_possible_score == 0:
        return 0, 0, vega, vm, other, 0.0

    latest_sem = max(scores_by_sem)
    session_score = scores_by_sem[latest_sem]
    total_score = sum(scores_by_sem.values())
    percent = round((total_score / max_possible_score) * 100, 2)

    return session_score, total_score, vega, vm, other, percent

def get_previous_results(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT stud_id, total_score, percent
            FROM ra_results
            """
        )

        rows = cur.fetchall()

    return {
        row[0]: {
            "total_score": row[1],
            "percent": row[2],
        }
        for row in rows
    }
def calculate_diff(previous_result, total_score, percent):
    if previous_result is None:
        return 0, 0.0

    diff_score = total_score - previous_result["total_score"]
    diff_percent = round(
        percent - previous_result["percent"],
        2,
    )

    return diff_score, diff_percent

def get_open_semester(marks_with_context):
    """
    Возвращает номер самого раннего семестра, где есть хотя бы одна незакрытая оценка.
    Закрытыми считаются только те семестры, где ВСЕ оценки входят в диапазон (-3, 3, 4, 5).
    """
    

    sem_grades = defaultdict(list)

    for mark in marks_with_context:
        grade = mark["grade"]
        sem = mark["sem"]
        sem_grades[sem].append(grade)

    open_sems = []

    for sem, grades in sem_grades.items():
        if any(g not in (-3, 3, 4, 5) for g in grades if g is not None):
            open_sems.append(sem)

    return min(open_sems) if open_sems else 0

def collect_ra_results(conn, sem, version_id):
    """
    Возвращает список словарей с результатами для всех студентов.
    """

    marks = get_marks_with_context(
        conn,
        version_id,
    )

    previous_results = get_previous_results(conn)

    marks_by_student = defaultdict(list)

    for mark in marks:
        marks_by_student[mark["stud_id"]].append(mark)

    results = []

    for stud_id, student_marks in marks_by_student.items():
        session_score, total_score, vega, vm, other, percent = (
            calculate_scores_and_departments_with_percent(student_marks)
        )

        previous_result = previous_results.get(stud_id)

        diff_score, diff_percent = calculate_diff(
            previous_result,
            total_score,
            percent,
        )

        open_sem = get_open_semester(student_marks)

        results.append({
            "stud_id": stud_id,
            "cur_sem": sem,
            "open_sem": open_sem,
            "session_score": session_score,
            "total_score": total_score,
            "diff_score": diff_score,
            "vega": vega,
            "vm": vm,
            "other": other,
            "percent": percent,
            "diff_percent": diff_percent,
        })

    return results

def insert_ra_results(conn, sem, version_id):
    results = collect_ra_results(conn, sem, version_id)

    results.sort(key=lambda r: r["percent"], reverse=True)

    with conn.cursor() as cur:
        for position, row in enumerate(results, start=1):
            cur.execute(
                """
                INSERT INTO ra_results (
                    position,
                    stud_id,
                    cur_sem,
                    open_sem,
                    session_score,
                    total_score,
                    diff_score,
                    vega,
                    vm,
                    other,
                    percent,
                    diff_percent
                )
                VALUES (
                    %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
                ON CONFLICT (stud_id)
                DO UPDATE SET
                    position = EXCLUDED.position,
                    cur_sem = EXCLUDED.cur_sem,
                    open_sem = EXCLUDED.open_sem,
                    session_score = EXCLUDED.session_score,
                    total_score = EXCLUDED.total_score,
                    diff_score = EXCLUDED.diff_score,
                    vega = EXCLUDED.vega,
                    vm = EXCLUDED.vm,
                    other = EXCLUDED.other,
                    percent = EXCLUDED.percent,
                    diff_percent = EXCLUDED.diff_percent
                """,
                (
                    position,
                    row["stud_id"],
                    row["cur_sem"],
                    row["open_sem"],
                    row["session_score"],
                    row["total_score"],
                    row["diff_score"],
                    row["vega"],
                    row["vm"],
                    row["other"],
                    row["percent"],
                    row["diff_percent"],
                ),
            )