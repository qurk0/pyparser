import pytest

from html_parser import parse_html
from models import ParsedReport

from pathlib import Path

from html_parser import parse_html


FIXTURES_DIR = Path(__file__).parent / "fixtures"

@pytest.fixture
def report():
    return parse_html(FIXTURES_DIR / "test.html")

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

    assert student.id == "21К0001"
    assert student.name == "Тестов А.А."

def test_parse_html_first_grade(report):
    grade = report.students[0].grades[0]

    assert grade.value == -3