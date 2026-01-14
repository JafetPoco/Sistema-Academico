import pytest
from unittest.mock import Mock

from app.domain.services.course_service import CourseService


def test_get_courses_by_professor_invalid_id():
    service = CourseService(Mock())

    with pytest.raises(ValueError, match="ID de profesor inválido"):
        service.get_courses_by_professor(0)


def test_get_courses_by_professor_filters_invalid_names():
    repo = Mock()
    repo.get_courses_by_professor.return_value = (
        [{"id": 1, "name": "Math"}, {"id": 2, "name": " "}, {"id": 3, "name": None}],
        None,
    )
    service = CourseService(repo)

    result = service.get_courses_by_professor(1)

    assert result == [{"id": 1, "name": "Math"}]


def test_get_courses_by_professor_repo_error():
    repo = Mock()
    repo.get_courses_by_professor.return_value = ([], "db error")
    service = CourseService(repo)

    with pytest.raises(RuntimeError, match="db error"):
        service.get_courses_by_professor(2)


def test_get_all_courses_success():
    repo = Mock()
    repo.get_all_courses.return_value = ([{"id": 1}], None)
    service = CourseService(repo)

    assert service.get_all_courses() == [{"id": 1}]


def test_get_all_courses_error():
    repo = Mock()
    repo.get_all_courses.return_value = ([], "oops")
    service = CourseService(repo)

    with pytest.raises(RuntimeError, match="oops"):
        service.get_all_courses()