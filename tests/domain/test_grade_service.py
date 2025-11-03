from types import SimpleNamespace
from unittest.mock import Mock

from app.domain.entities import Grade
from app.domain.services.grade_service import GradeService


def test_parent_grades_aggregate():
    grade_repo = Mock()
    course_repo = Mock()
    student_repo = Mock()

    student_repo.get_by_parent_id.return_value = [
    SimpleNamespace(user_id=1, user=SimpleNamespace(full_name="Alumno Uno"))
    ]
    grade_repo.get_by_student_id.return_value = [
        Grade(grade_id="g1", student_id=1, course_id=101, score=16)
    ]
    course_repo.get.return_value = SimpleNamespace(name="Matematicas")

    service = GradeService(
        grade_repository=grade_repo,
        course_repository=course_repo,
        student_repository=student_repo,
    )

    result = service.get_grades_by_parent_id(parent_id=77)

    assert result == [
        {
            "id": 1,
            "name": "Alumno Uno",
            "grades": [
                {
                    "score": 16,
                    "course_name": "Matematicas",
                }
            ],
        }
    ]

    student_repo.get_by_parent_id.assert_called_once_with(77)
    grade_repo.get_by_student_id.assert_called_once_with(1)
    course_repo.get.assert_called_once_with(101)


def test_parent_grades_missing_course():
    grade_repo = Mock()
    course_repo = Mock()
    student_repo = Mock()

    student_repo.get_by_parent_id.return_value = [
        SimpleNamespace(user_id=2, user=SimpleNamespace(full_name="Alumno Dos"))
    ]
    grade_repo.get_by_student_id.return_value = [
        Grade(grade_id="g2", student_id=2, course_id=999, score=11)
    ]
    course_repo.get.return_value = None

    service = GradeService(
        grade_repository=grade_repo,
        course_repository=course_repo,
        student_repository=student_repo,
    )

    result = service.get_grades_by_parent_id(parent_id=10)

    assert result[0]["grades"] == [
        {
            "score": 11,
            "course_name": "Curso Desconocido",
        }
    ]
