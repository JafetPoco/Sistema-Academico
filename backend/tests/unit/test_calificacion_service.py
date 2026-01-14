import pytest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.domain.services.calificacion_service import CalificacionService


@pytest.fixture
def calificacion_service():
    repo = Mock()
    return CalificacionService(repo), repo


def test_calificate_student_success(calificacion_service):
    service, repo = calificacion_service
    repo.add.return_value = ("grade", None)

    with patch("app.domain.services.calificacion_service.uuid.uuid4", return_value="uuid"):
        result = service.calificate_student({"student_id": 1, "course_id": 2, "score": 18})

    assert result == "grade"
    grade = repo.add.call_args.args[0]
    assert grade.grade_id == "uuid"
    assert grade.student_id == 1
    assert grade.course_id == 2
    assert grade.score == 18


def test_calificate_student_raises_on_error(calificacion_service):
    service, repo = calificacion_service
    repo.add.return_value = (None, "db error")

    with pytest.raises(ValueError, match="db error"):
        service.calificate_student({"student_id": 1, "course_id": 2, "score": 18})


def test_ver_calificaciones_delegates(calificacion_service):
    service, _ = calificacion_service
    proxy = Mock()
    proxy.obtener_calificaciones_por_estudiante.return_value = ["grade"]

    result = service.ver_calificaciones(3, proxy)

    assert result == ["grade"]
    proxy.obtener_calificaciones_por_estudiante.assert_called_once_with(3)


def test_obtener_calificaciones_por_estudiante_filters(calificacion_service):
    service, repo = calificacion_service
    repo.list_all.return_value = [
        SimpleNamespace(student_id=1),
        SimpleNamespace(student_id=2),
        SimpleNamespace(student_id=1),
    ]

    results = service.obtener_calificaciones_por_estudiante(1)

    assert [grade.student_id for grade in results] == [1, 1]