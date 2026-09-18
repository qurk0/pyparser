from unittest.mock import MagicMock

from ra_results import (
    calculate_scores_and_departments_with_percent,
    calculate_diffs,
    get_open_semester,
)


def test_calculate_scores():
    marks = [
        {
            "sem": 1,
            "form": 1,
            "max_grade": -3,
            "department_id": 1,
            "grade": 3,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 2,
            "grade": 4,
        },
        {
            "sem": 2,
            "form": 3,
            "max_grade": 5,
            "department_id": 5,
            "grade": 5,
        },
    ]

    result = calculate_scores_and_departments_with_percent(marks)

    assert result == (5, 12, 3, 4, 5, 92.31)


def test_absence_marks_are_ignored():
    marks = [
        {
            "sem": 1,
            "form": 1,
            "max_grade": -3,
            "department_id": 1,
            "grade": -9,
        },
        {
            "sem": 1,
            "form": 1,
            "max_grade": -3,
            "department_id": 1,
            "grade": -7,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 2,
            "grade": 5,
        },
    ]

    result = calculate_scores_and_departments_with_percent(marks)

    assert result == (5, 5, 0, 5, 0, 100.0)


def test_pass_grade_is_counted_as_three_points():
    marks = [
        {
            "sem": 1,
            "form": 1,
            "max_grade": -3,
            "department_id": 1,
            "grade": -3,
        },
    ]

    result = calculate_scores_and_departments_with_percent(marks)

    assert result == (3, 3, 3, 0, 0, 100.0)


def test_departments_are_calculated_separately():
    marks = [
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 5,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 3,
            "grade": 4,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 2,
            "grade": 3,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 4,
            "grade": 5,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 5,
            "grade": 4,
        },
    ]

    result = calculate_scores_and_departments_with_percent(marks)

    assert result[2] == 9
    assert result[3] == 8
    assert result[4] == 4


def test_latest_semester_is_used_for_session_score():
    marks = [
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 3,
        },
        {
            "sem": 2,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 5,
        },
    ]

    result = calculate_scores_and_departments_with_percent(marks)

    assert result[0] == 5
    assert result[1] == 8


def test_get_open_semester_returns_open_semester():
    marks = [
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 5,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 3,
        },
        {
            "sem": 2,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 0,
        },
    ]

    assert get_open_semester(marks) == 2


def test_get_open_semester_returns_zero_when_all_marks_are_closed():
    marks = [
        {
            "sem": 1,
            "form": 1,
            "max_grade": -3,
            "department_id": 1,
            "grade": -3,
        },
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 5,
        },
        {
            "sem": 2,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 4,
        },
    ]

    assert get_open_semester(marks) == 0


def test_get_open_semester_returns_earliest_open_semester():
    marks = [
        {
            "sem": 1,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 0,
        },
        {
            "sem": 2,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": 3,
        },
        {
            "sem": 3,
            "form": 3,
            "max_grade": 5,
            "department_id": 1,
            "grade": -7,
        },
    ]

    assert get_open_semester(marks) == 1


def test_calculate_diffs():
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = (10, 80.0)

    result = calculate_diffs(
        conn=conn,
        stud_id=42,
        total_score=15,
        percent=90.5,
    )

    assert result == (5, 10.5)


def test_calculate_diffs_can_be_negative():
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = (20, 95.0)

    result = calculate_diffs(
        conn=conn,
        stud_id=42,
        total_score=15,
        percent=90.5,
    )

    assert result == (-5, -4.5)


def test_calculate_diffs_returns_zero_without_previous_result():
    conn = MagicMock()
    cursor = conn.cursor.return_value.__enter__.return_value
    cursor.fetchone.return_value = None

    result = calculate_diffs(
        conn=conn,
        stud_id=42,
        total_score=15,
        percent=90.5,
    )

    assert result == (0, 0.0)