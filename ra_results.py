def get_student_marks_with_context(conn, stud_id):
    """
    Получает все оценки студента по последней версии с деталями:
    - семестр (по ключу "sem")
    - форма контроля (по ключу "form")
    - max_grade (по ключу "max_grade")
    - кафедра дисциплины (по ключу "department_id")
    - оценка (по ключу "grade")
    """
    with conn.cursor() as cur:
        # Получаем последнюю версию
        cur.execute("SELECT id FROM ra_version ORDER BY created DESC LIMIT 1")
        version_id = cur.fetchone()[0]

        # Получаем оценки с контекстом
        cur.execute("""
            SELECT 
                rc.sem,
                rc.form,
                rc.max_grade,
                rd.department_id,
                rm.grade
            FROM ra_mark rm
            JOIN ra_control rc ON rm.control_id = rc.id
            JOIN ra_disc rd ON rc.disc_id = rd.id
            WHERE rm.version_id = %s AND rm.stud_id = %s
        """, (version_id, stud_id))

        rows = cur.fetchall()
        return [
            {
                "sem": row[0],
                "form": row[1],
                "max_grade": row[2],
                "department_id": row[3],
                "grade": row[4]
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
    from collections import defaultdict

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

def calculate_diffs(conn, stud_id, total_score, percent):
    """
    Считает:
    - diff_score: разница с тем, что уже записано в ra_results.total_score
    - diff_percent: разница с ra_results.percent
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT total_score, percent
            FROM ra_results
            WHERE stud_id = %s
        """, (stud_id,))
        row = cur.fetchone()

        if not row:
            return 0, 0.0  # Нет предыдущих данных — считать не с чем

        prev_total_score, prev_percent = row
        diff_score = total_score - prev_total_score
        diff_percent = round(percent - prev_percent, 2)

        return diff_score, diff_percent

# def get_current_semester(marks_with_context):
#     """
#     Возвращает максимальный (текущий) семестр, в котором у студента есть хотя бы одна оценка.
#     """
#     semesters = {mark["sem"] for mark in marks_with_context if mark["grade"] is not None}
#     return max(semesters) if semesters else 0

def get_open_semester(marks_with_context):
    """
    Возвращает номер самого раннего семестра, где есть хотя бы одна незакрытая оценка.
    Закрытыми считаются только те семестры, где ВСЕ оценки входят в диапазон (-3, 3, 4, 5).
    """
    from collections import defaultdict

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

def collect_ra_results(conn, sem):
    """
    Возвращает список словарей с результатами для всех студентов.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM students")
        student_ids = [row[0] for row in cur.fetchall()]

    results = []

    for stud_id in student_ids:
        marks = get_student_marks_with_context(conn, stud_id)
        session_score, total_score, vega, vm, other, percent = calculate_scores_and_departments_with_percent(marks)
        diff_score, diff_percent = calculate_diffs(conn, stud_id, total_score, percent)
        open_sem = get_open_semester(marks)

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
            "diff_percent": diff_percent
        })

    return results

def insert_ra_results(conn, sem):
    """
    Обновляет или добавляет результаты в ra_results для каждого студента.
    """
    results = collect_ra_results(conn, sem)

    # Сортировка по percent DESC для расчёта позиции в рейтинге
    results.sort(key=lambda r: r["percent"], reverse=True)

    with conn.cursor() as cur:
        for position, row in enumerate(results, start=1):
            # Проверяем, есть ли запись по stud_id
            cur.execute("""
                SELECT 1 FROM ra_results WHERE stud_id = %s
            """, (row["stud_id"],))
            exists = cur.fetchone()

            if exists:
                # Обновляем
                cur.execute("""
                    UPDATE ra_results
                    SET 
                        position = %s,
                        cur_sem = %s,
                        open_sem = %s,
                        session_score = %s,
                        total_score = %s,
                        diff_score = %s,
                        vega = %s,
                        vm = %s,
                        other = %s,
                        percent = %s,
                        diff_percent = %s
                    WHERE stud_id = %s
                """, (
                    position, row["cur_sem"], row["open_sem"],
                    row["session_score"], row["total_score"], row["diff_score"],
                    row["vega"], row["vm"], row["other"],
                    row["percent"], row["diff_percent"], row["stud_id"]
                ))
            else:
                # Вставляем новую запись
                cur.execute("""
                    INSERT INTO ra_results (
                        position, stud_id, cur_sem, open_sem,
                        session_score, total_score, diff_score,
                        vega, vm, other, percent, diff_percent
                    ) VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s, %s
                    )
                """, (
                    position, row["stud_id"], row["cur_sem"], row["open_sem"],
                    row["session_score"], row["total_score"], row["diff_score"],
                    row["vega"], row["vm"], row["other"],
                    row["percent"], row["diff_percent"]
                ))

    conn.commit()
