import pytest
from unittest.mock import Mock

from app.domain.services.student_service import StudentService


def test_get_all_students_with_name_filters():
    repo = Mock()
    repo.get_students_with_names.return_value = (
        [{"id": 1, "name": "Ana"}, {"id": 2, "name": " "}],
        None,
    )
    service = StudentService(repo)

    result = service.get_all_students_with_name()

    assert result == [{"id": 1, "name": "Ana"}]


def test_get_all_students_with_name_error():
    repo = Mock()
    repo.get_students_with_names.return_value = ([], "db error")
    service = StudentService(repo)

    with pytest.raises(RuntimeError, match="db error"):
        service.get_all_students_with_name()


def test_get_all_students():
    repo = Mock()
    repo.list_all.return_value = ["student"]
    service = StudentService(repo)

    assert service.get_all_students() == ["student"]


def test_obtener_estudiante_por_id():
    repo = Mock()
    repo.get.return_value = "student"
    service = StudentService(repo)

    assert service.obtener_estudiante_por_id(9) == "student"