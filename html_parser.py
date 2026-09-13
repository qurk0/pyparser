from bs4 import BeautifulSoup
from normalization import GRADE_MAPPING, TYPE_MAPPING

from models import ParsedReport, Discipline, Control, Student, Grade

def normalize_grade(grade_text):
    grade_text = grade_text.strip()

    if grade_text not in GRADE_MAPPING:
        raise ValueError(f"Неизвестная оценка: '{grade_text}'")

    return GRADE_MAPPING[grade_text]

def parse_html(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Вытягиваем название группы
    group_name_element = soup.find("div", id= "groupJournalTabBlock")
    if group_name_element:
        group_name_text = group_name_element.get_text(strip=True)
        if "Группа обучающихся:" in group_name_text:
            group_name = group_name_text.split("Группа обучающихся:")[1].split("|")[0].strip()
        else:
            group_name = "Неизвестно"
    else:
        group_name = "Неизвестно"

    controls = []
    discipline_headers = soup.select(".v-text")
    for header in discipline_headers:
        text = header.get_text(strip=True).replace("\n", " ")
        if "№" in text:
            parts = text.split("№")
            title = parts[0].strip().replace("\n", " ")
            # disc_id = int(parts[1].strip())

            if title.endswith(" Д"):
                title = title[:-2].strip()

            if title.endswith(" ПП"):
                title = title[:-3].strip()

            parent_wrapper = header.find_parent(
                "div",
                class_="sh-simple-list-header-column-wrapper",
            )

            if not parent_wrapper:
                raise ValueError(
                    f"Не найден контейнер для дисциплины: {title}"
                )

            accreditation_type_element = parent_wrapper.find_previous_sibling(
                "div",
                class_="sh-simple-list-header-column-content",
            )

            if not accreditation_type_element:
                raise ValueError(
                    f"Не найден тип контроля для дисциплины: {title}"
                )

            accreditation_type_text = accreditation_type_element.get_text(strip=True)

            accreditation_type = TYPE_MAPPING.get(accreditation_type_text)

            if accreditation_type is None:
                raise ValueError(
                    f"Неизвестный тип контроля '{accreditation_type_text}' "
                    f"для дисциплины '{title}'"
                )

            discipline = Discipline(
                title=title,
            )

            control = Control(
                discipline=discipline,
                control_type=accreditation_type,
            )

            controls.append(control)

    # Парсинг студентов и их оценок
    students = []
    rows = soup.select(".sh-simple-list-row-odd, .sh-simple-list-row-even")
    for row in rows:
        student_id = row.select_one("td:nth-of-type(3)").get_text(strip=True)
        full_name = row.select_one("td:nth-of-type(2)").get_text(strip=True)
        grades = [normalize_grade(cell.get_text(strip=True)) for cell in row.select("td div.cell-link div")]

        # Связываем оценки с дисциплинами
        if len(grades) != len(controls):
            raise ValueError(
                f"Для студента '{full_name}' количество оценок "
                f"({len(grades)}) не совпадает с количеством контролей "
                f"({len(controls)})"
            )

        student_grades = [
            Grade(
                control=controls[i],
                value=grades[i],
            )
            for i in range(len(controls))
        ]

        students.append(
            Student(
                id=student_id,
                name=full_name,
                grades=student_grades,
            )
        )

    return ParsedReport(
        group_name=group_name,
        controls=controls,
        students=students,
    )

if __name__ == "__main__":
    report = parse_html("test.html")

    print(report.group_name)
    print(report.controls[:3])
    print(report.students[:2])
    print(
    report.students[0].grades[0].control
    is report.controls[0]
)