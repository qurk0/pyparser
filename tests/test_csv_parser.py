import pytest

from csv_parser import parse_csv
from models import ParsedReport

@pytest.fixture
def report():
    return parse_csv("test.csv")

def test_parse_csv_returns_parsed_report(report):
    assert isinstance(report, ParsedReport)


def test_parse_csv_group_name(report):
    assert report.group_name == "КММО-11-24"

def test_parse_csv_first_control(report):
    control = report.controls[0]

    assert control.discipline.title == "Дискретные математические модели"
    assert control.control_type == 1

def test_parse_csv_first_student(report):
    student = report.students[0]

    assert student.id == "24К1142"
    assert student.name == "Aaaaa Aaaa Aaa 32"

def test_parse_csv_first_grade(report):
    grade = report.students[0].grades[0]

    assert grade.value == -9