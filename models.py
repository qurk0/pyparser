from dataclasses import dataclass


@dataclass
class Discipline:
    title: str


@dataclass
class Control:
    discipline: Discipline
    control_type: int


@dataclass
class Grade:
    control: Control
    value: int | None


@dataclass
class Student:
    id: str
    name: str
    grades: list[Grade]


@dataclass
class ParsedReport:
    group_name: str
    controls: list[Control]
    students: list[Student]