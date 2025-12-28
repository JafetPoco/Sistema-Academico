from app.domain.entities import Course, User
from app.infrastructure.repository.repository import CourseRepository, UserRepository


def test_user_repository_create_and_retrieve(app_context):
    repo = UserRepository()
    with app_context.app_context():
        user = User(
            user_id=None,
            full_name="Juan Perez",
            email="juan@example.com",
            password_hash="hash",
            role=1,
        )

        saved_user, error = repo.create(user)

        assert error is None
        assert saved_user.user_id is not None

        fetched = repo.find_by_email("juan@example.com")
        assert fetched is not None
        assert fetched.email == "juan@example.com"


def test_user_repository_list_by_role(app_context):
    repo = UserRepository()
    with app_context.app_context():
        admin = User(
            user_id=None,
            full_name="Admin",
            email="admin@example.com",
            password_hash="hash",
            role=2,
        )
        student = User(
            user_id=None,
            full_name="Estudiante",
            email="student@example.com",
            password_hash="hash",
            role=0,
        )

        repo.create(admin)
        repo.create(student)

        admins = repo.list_by_role(2)

        assert len(admins) == 1
        assert admins[0].email == "admin@example.com"


def test_course_repository_get_courses_by_professor(app_context):
    user_repo = UserRepository()
    course_repo = CourseRepository()
    with app_context.app_context():
        professor_user = User(
            user_id=None,
            full_name="Profesor",
            email="prof@example.com",
            password_hash="hash",
            role=3,
        )
        professor_saved, _ = user_repo.create(professor_user)

        course = Course(
            course_id=None,
            name="Calculo",
            professor_id=professor_saved.user_id,
        )
        course_repo.add(course)

        courses, error = course_repo.get_courses_by_professor(professor_saved.user_id)

        assert error is None
        assert len(courses) == 1
        assert courses[0]["name"] == "Calculo"
