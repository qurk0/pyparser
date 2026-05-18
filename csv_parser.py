from normalization import GRADE_MAPPING
import pandas as pd
import json

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
    disciplines = []
    for col in range(discipline_start_col, discipline_end_col):
        value = df.iloc[6, col]
        if pd.notna(value):
            parts = value.split(", ")
            if len(parts) == 2:
                title, dtype = parts
            else:
                title = value
                dtype = "Неизвестно"
            disciplines.append({"title": title.strip(), "type": dtype.strip()})

    # Извлечение студентов с оценками
    students = []
    for i in range(7, df.shape[0]):
        student_id = df.iloc[i, 1]
        name = df.iloc[i, 2]
        if pd.isna(name):
            break

        grades = []
        for j, discipline in enumerate(disciplines):
            col = j + discipline_start_col
            grade = df.iloc[i, col]
            if pd.notna(grade) and str(grade).strip() != "":
                if grade == "х" or grade == "x":
                    grade = ""
                grade = GRADE_MAPPING.get(grade, grade)
                grades.append({
                    "discipline": discipline["title"],
                    "type": discipline["type"],
                    "grade": str(grade).strip()
                })

        students.append({
            "id": str(student_id).strip(),
            "name": str(name).strip(),
            "grades": grades
        })

    return {
        "group_name": group_name,
        "disciplines": disciplines,
        "students": students
    }

# Пример использования:
if __name__ == "__main__":
    result = parse_csv("test.csv")
    print(json.dumps(result, ensure_ascii=False, indent=2))
