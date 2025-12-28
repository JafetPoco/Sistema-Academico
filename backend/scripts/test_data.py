import logging
from werkzeug.security import generate_password_hash
from app import create_app
from app.domain.entities import (
    User,
    Admin,
    Professor,
    Parent,
    Student,
    Course,
    Grade,
    Enrollment,
)
from app.infrastructure.repository.models import CourseDTO, EnrollmentDTO
from app.infrastructure.repository.repository import (
    UserRepository,
    AdminRepository,
    ProfessorRepository,
    ParentRepository,
    StudentRepository,
    CourseRepository,
    GradeRepository,
    EnrollmentRepository,
)
from app.infrastructure.repository.mapper import CourseMapper
from app.domain.services.auth_service import AuthService

logging.basicConfig(level=logging.INFO)

USER_FIXTURES = [
    {
        "email": "admin@prueba.com",
        "name": "Administrador Selenium",
        "password": "admin",
        "role": AuthService.ADMIN_ROLE,
    },
    {
        "email": "professor@test.com",
        "name": "Profesor Selenium",
        "password": "professor",
        "role": AuthService.TEACHER_ROLE,
    },
    {
        "email": "parent@test.com",
        "name": "Padre Selenium",
        "password": "parent",
        "role": AuthService.PARENT_ROLE,
    },
    {
        "email": "noActivate@test.com",
        "name": "Usuario No Activo",
        "password": "noActivate",
        "role": AuthService.UNKNOWN_ROLE,
    },
    {
        "email": "student@test.com",
        "name": "Estudiante de Prueba",
        "password": "student",
        "role": AuthService.UNKNOWN_ROLE,
    },
]
GRADE_ID = "seed-grade-child-course"
COURSE_NAME = "Curso Selenium"


def ensure_user(user_repo: UserRepository, email: str, full_name: str, password: str, role: int) -> User:
    existing = user_repo.find_by_email(email)
    if existing:
        if existing.role != role:
            user_repo.update(existing.user_id, {"role": role})
        return existing

    hashed = generate_password_hash(password)
    logger = logging.getLogger(__name__)
    user = User(
        user_id=None,
        full_name=full_name,
        email=email,
        password_hash=hashed,
        role=role,
    )
    created, error = user_repo.create(user)
    if error:
        logger.error("No se pudo crear el usuario %s: %s", email, error)
        raise SystemExit(error)

    logger.info("Usuario creado: %s", email)
    return created


def ensure_relation(repository, entity, entity_id):
    if repository.get(entity_id):
        return

    _, error = repository.add(entity)
    if error:
        raise SystemExit(f"No se pudo añadir la relación: {error}")


def ensure_student(student_repo: StudentRepository, child_user: User, parent_user: User):
    existing = student_repo.get(child_user.user_id)

    if existing:
        if existing.parent_id != parent_user.user_id:
            student_repo.update(child_user.user_id, {"parent_id": parent_user.user_id})
        return

    _, error = student_repo.add(Student(child_user.user_id, parent_user.user_id))
    if error:
        raise SystemExit(f"No se pudo añadir el estudiante: {error}")


def ensure_course(course_repo: CourseRepository, professor_id: int) -> Course:
    existing = CourseDTO.query.filter_by(name=COURSE_NAME, professor_id=professor_id).first()
    if existing:
        return CourseMapper.to_domain(existing)

    created, error = course_repo.add(Course(None, COURSE_NAME, professor_id))
    if error:
        raise SystemExit(f"No se pudo crear el curso: {error}")
    return created


def ensure_enrollment(enrollment_repo: EnrollmentRepository, user_id: int, course_id: int):
    existing = EnrollmentDTO.query.filter_by(user_id=user_id, course_id=course_id).first()
    if existing:
        return

    _, error = enrollment_repo.add(Enrollment(None, user_id, course_id))
    if error:
        raise SystemExit(f"No se pudo crear la matrícula: {error}")


def ensure_grade(grade_repo: GradeRepository, student_id: int, course_id: int):
    existing = grade_repo.get(GRADE_ID)
    if existing:
        return

    _, error = grade_repo.add(Grade(GRADE_ID, student_id, course_id, 16))
    if error:
        raise SystemExit(f"No se pudo crear la calificación: {error}")


def seed_data():
    app = create_app()
    with app.app_context():
        user_repo = UserRepository()
        admin_repo = AdminRepository()
        professor_repo = ProfessorRepository()
        parent_repo = ParentRepository()
        student_repo = StudentRepository()
        course_repo = CourseRepository()
        grade_repo = GradeRepository()
        enrollment_repo = EnrollmentRepository()

        seeded_users = {}
        for fixture in USER_FIXTURES:
            user = ensure_user(
                user_repo,
                fixture["email"],
                fixture["name"],
                fixture["password"],
                fixture["role"],
            )
            seeded_users[fixture["email"]] = user

        ensure_relation(admin_repo, Admin(seeded_users["admin@prueba.com"].user_id), seeded_users["admin@prueba.com"].user_id)
        ensure_relation(professor_repo, Professor(seeded_users["professor@test.com"].user_id), seeded_users["professor@test.com"].user_id)
        ensure_relation(parent_repo, Parent(seeded_users["parent@test.com"].user_id), seeded_users["parent@test.com"].user_id)

        ensure_student(
            student_repo,
            seeded_users["student@test.com"],
            seeded_users["parent@test.com"],
        )

        course = ensure_course(course_repo, seeded_users["professor@test.com"].user_id)
        ensure_enrollment(enrollment_repo, seeded_users["student@test.com"].user_id, course.course_id)
        ensure_grade(grade_repo, seeded_users["student@test.com"].user_id, course.course_id)

        logging.getLogger(__name__).info("Datos de prueba sembrados correctamente.")


if __name__ == "__main__":
    seed_data()
