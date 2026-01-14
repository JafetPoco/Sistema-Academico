import pytest
from unittest.mock import patch

from app.domain.services.enrollment_service import EnrollmentService


@pytest.fixture
def enrollment_service():
    with patch("app.domain.services.enrollment_service.EnrollmentRepository") as enrollment_cls, \
        patch("app.domain.services.enrollment_service.UserRepository") as user_cls, \
        patch("app.domain.services.enrollment_service.CourseRepository") as course_cls, \
        patch("app.domain.services.enrollment_service.GradeRepository") as grade_cls:
        enrollment_repo = enrollment_cls.return_value
        course_repo = course_cls.return_value
        grade_repo = grade_cls.return_value
        service = EnrollmentService()
        service.enrollment_repo = enrollment_repo
        service.course_repo = course_repo
        service.grade_repo = grade_repo
        yield service, enrollment_repo, course_repo, grade_repo


def test_get_students_enrolled_in_course_formats(enrollment_service):
    service, enrollment_repo, _, _ = enrollment_service
    enrollment_repo.get_course_students_with_names.return_value = (
        [{"id": 1, "name": "Ana"}, {"id": 2, "name": "Luis"}],
        None,
    )

    students, error = service.get_students_enrolled_in_course(1)

    assert error is None
    assert students == [{"id": 1, "name": "Ana"}, {"id": 2, "name": "Luis"}]


def test_get_students_enrolled_in_course_error(enrollment_service):
    service, enrollment_repo, _, _ = enrollment_service
    enrollment_repo.get_course_students_with_names.return_value = ([], "db error")

    students, error = service.get_students_enrolled_in_course(1)

    assert students == []
    assert error == "db error"


def test_validate_professor_course_access_forbidden(enrollment_service):
    service, _, course_repo, _ = enrollment_service
    course_repo.get_courses_by_professor.return_value = ([{"id": 1}], None)

    allowed, error = service.validate_professor_course_access(7, 99)

    assert allowed is False
    assert "permisos" in error


def test_get_professor_courses_with_student_counts(enrollment_service):
    service, enrollment_repo, course_repo, grade_repo = enrollment_service
    course_repo.get_courses_by_professor.return_value = (
        [{"id": 3, "name": "Science"}],
        None,
    )
    enrollment_repo.count_students_by_course.return_value = 12
    grade_repo.get_average_by_course_id.return_value = 15.5

    courses, error = service.get_professor_courses_with_student_counts(2)

    assert error is None
    assert courses == [
        {
            "id": 3,
            "nombre": "Science",
            "student_count": 12,
            "average_score": 15.5,
        }
    ]