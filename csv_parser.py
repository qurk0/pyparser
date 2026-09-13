import pandas as pd

from normalization import GRADE_MAPPING, TYPE_MAPPING
from models import ParsedReport, Grade, Student, Discipline, Control

def parse_csv(file_path: str):
    df = pd.read_csv(file_path, encoding="cp1251", sep=";", header=None)

    # Название группы (строка 3, колонка 2)
    group_name = df.iloc[3, 2]

    # Поиск границ списка дисциплин по строке 5
    discipline_start_col = 5
    discipline_end_col = discipline_start_col
    for col in range(discipline_start_col, df.shape[1]):
        cell = str(df.iloc[5, col])
        if cell.strip() == '' or 'оценок' in cell.lower() or 'средний' in cell.lower():
            break
        discipline_end_col += 1

    # Извлечение дисциплин из строки 6
    controls = []
    for col in range(discipline_start_col, discipline_end_col):
        value = df.iloc[6, col]
        if pd.notna(value):
            title, dtype = str(value).rsplit(", ", 1)
            control_type = TYPE_MAPPING.get(dtype.strip())

            if control_type is None:
                raise ValueError(
                    f"Неизвестный тип контроля '{dtype}' "
                    f"для дисциплины '{title}'"
                )
                
            discipline = Discipline(
                title=title.strip(),
            )

            control = Control(
                discipline = discipline,
                control_type = control_type,
            )

            controls.append(control)

    # Извлечение студентов с оценками
    students = []
    for i in range(7, df.shape[0]):
        student_id = df.iloc[i, 1]
        name = df.iloc[i, 2]
        if pd.isna(name):
            break

        student_grades = []

    for j, control in enumerate(controls):
        col = j + discipline_start_col
        raw_grade = df.iloc[i, col]

        if pd.isna(raw_grade):
            grade_text = ""
        else:
            grade_text = str(raw_grade).strip()

        # В CSV строчные x/х означают отсутствие оценки
        if grade_text in ("х", "x"):
            grade_text = ""

        if grade_text not in GRADE_MAPPING:
            raise ValueError(
                f"Неизвестная оценка '{grade_text}' "
                f"у студента '{name}'"
            )

        grade_value = GRADE_MAPPING[grade_text]

        student_grades.append(
            Grade(
                control=control,
                value=grade_value,
            )
        )

    students.append(
        Student(
            id=str(student_id).strip(),
            name=str(name).strip(),
            grades=student_grades,
        )
    )

    return ParsedReport(
        group_name=str(group_name).strip(),
        controls=controls,
        students=students,
    )

# Пример использования:
if __name__ == "__main__":
    report = parse_csv("test.csv")

    print(report.group_name)
    print(report.controls[:5])
    print(report.students[:2])