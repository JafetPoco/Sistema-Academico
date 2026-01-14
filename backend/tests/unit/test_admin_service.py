import pytest
from types import SimpleNamespace
from unittest.mock import patch

from app.domain.services.admin_service import AdminService


@pytest.fixture
def admin_service():
    with patch("app.domain.services.admin_service.UserRepository") as user_repo_cls, \
        patch("app.domain.services.admin_service.CourseRepository") as course_repo_cls:
        user_repo = user_repo_cls.return_value
        course_repo = course_repo_cls.return_value
        service = AdminService()
        service.user_repository = user_repo
        service.course_repository = course_repo
        yield service, user_repo, course_repo


def test_update_user_success(admin_service):
    service, user_repo, _ = admin_service
    user_repo.get.return_value = SimpleNamespace(user_id=10, role=2)

    result = service.update_user(10, 3)

    assert result is True
    user_repo.update.assert_called_once_with(10, {"role": 3})


def test_update_user_missing(admin_service):
    service, user_repo, _ = admin_service
    user_repo.get.return_value = None

    result = service.update_user(99, 2)

    assert result is False
    user_repo.update.assert_not_called()


def test_get_users(admin_service):
    service, user_repo, _ = admin_service
    user_repo.list_all.return_value = ["user"]

    assert service.get_users() == ["user"]

def test_create_course(admin_service):
    service, _, course_repo = admin_service
    course_repo.add.return_value = ("course", None)

    result = service.create_course({"name": "Math", "professor_id": 7})

    assert result == ("course", None)
    added_course = course_repo.add.call_args.args[0]
    assert added_course.name == "Math"
    assert added_course.professor_id == 7


def test_get_courses(admin_service):
    service, _, course_repo = admin_service
    course_repo.list_all.return_value = ["course"]

    assert service.get_courses() == ["course"]


def test_get_professors(admin_service):
    service, user_repo, _ = admin_service
    user_repo.list_by_role.return_value = ["professor"]

    assert service.get_professors() == ["professor"]
    user_repo.list_by_role.assert_called_once_with(role=1)