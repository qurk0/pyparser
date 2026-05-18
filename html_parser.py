from bs4 import BeautifulSoup
from normalization import GRADE_MAPPING, TYPE_MAPPING

def normalize_grade(grade_text):
    return GRADE_MAPPING.get(grade_text.strip(), None)

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

    disciplines = []
    discipline_headers = soup.select(".v-text")
    for header in discipline_headers:
        text = header.get_text(strip=True).replace("\n", " ")
        if "№" in text:
            parts = text.split("№")
            title = parts[0].strip().replace("\n", " ")
            disc_id = int(parts[1].strip())

            if title.endswith(" Д"):
                title = title[:-2].strip()

            if title.endswith(" ПП"):
                title = title[:-3].strip()

            parent_wrapper = header.find_parent("div", class_="sh-simple-list-header-column-wrapper")
            if parent_wrapper:
                accreditation_type_element = parent_wrapper.find_previous_sibling("div", class_="sh-simple-list-header-column-content")
                if accreditation_type_element:
                    accreditation_type = accreditation_type_element.get_text(strip=True)
                    accreditation_type = TYPE_MAPPING.get(accreditation_type, "Неизвестно")
                else:
                    accreditation_type = "Неизвестно"
            else:
                accreditation_type = "Неизвестно"

            disciplines.append({"id": disc_id, "title": title, "type": accreditation_type})

    # Парсинг студентов и их оценок
    students = []
    rows = soup.select(".sh-simple-list-row-odd, .sh-simple-list-row-even")
    for row in rows:
        student_id = row.select_one("td:nth-of-type(3)").get_text(strip=True)
        full_name = row.select_one("td:nth-of-type(2)").get_text(strip=True)
        grades = [normalize_grade(cell.get_text(strip=True)) for cell in row.select("td div.cell-link div")]

        # Связываем оценки с дисциплинами
        grades_with_disciplines = [
            {"discipline": disciplines[i]["title"], "type": disciplines[i]["type"], "grade": grades[i]}
            for i in range(len(disciplines))
        ]

        students.append({"id": student_id, "name": full_name, "grades": grades_with_disciplines})

    return group_name, disciplines, students

if __name__ == "__main__":
    group_name, disciplines, students = parse_html("страница_бакалавры.html")
    print(students)