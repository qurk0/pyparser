import pytest

from html_parser import parse_html
from models import ParsedReport

@pytest.fixture
def report():
    return parse_html("test.html")

def test_parse_html_returns_parsed_report(report):
    assert isinstance(report, ParsedReport)


def test_parse_html_group_name(report):
    assert report.group_name == "КМБО-02-21"

def test_parse_html_first_control(report):
    control = report.controls[0]

    assert control.discipline.title == "Психология и педагогика"
    assert control.control_type == 1

def test_parse_html_first_student(report):
    student = report.students[0]

    assert student.id == "21К0522"
    assert student.name == "Александров П.В."

def test_parse_html_first_grade(report):
    grade = report.students[0].grades[0]

    assert grade.value == -3