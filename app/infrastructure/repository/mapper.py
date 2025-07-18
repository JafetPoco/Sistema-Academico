# infrastructure/repository/mapper.py

from domain.entities import (
    User,
    Announcement,
    Grade,
    Parent,
    Course,
    Student,
    Admin,
    Professor
)

from infrastructure.repository.models import (
    UserDTO,
    AnnouncementDTO,
    GradeDTO,
    ParentDTO,
    CourseDTO,
    StudentDTO,
    AdminDTO,
    ProfessorDTO
)

class UserMapper:
    @staticmethod
    def to_domain(dto: UserDTO) -> User:
        return User(
            user_id=dto.user_id,
            full_name=dto.full_name,
            email=dto.email,
            password_hash=dto.password_hash,
            role=dto.role
        )

    @staticmethod
    def to_dto(domain: User) -> UserDTO:
        return UserDTO(
            user_id=domain.user_id,
            full_name=domain.full_name,
            email=domain.email,
            password_hash=domain.password_hash,
            role=domain.role
        )

class AnnouncementMapper:
    @staticmethod
    def to_domain(dto: AnnouncementDTO) -> Announcement:
        return Announcement(
            announcement_id=dto.announcement_id,
            course_id=dto.course_id,
            user_id=dto.user_id,
            title=dto.title,
            content=dto.content,
            created_at=dto.created_at
        )

    @staticmethod
    def to_dto(domain: Announcement) -> AnnouncementDTO:
        return AnnouncementDTO(
            announcement_id=domain.announcement_id,
            course_id=domain.course_id,
            user_id=domain.user_id,
            title=domain.title,
            content=domain.content,
            created_at=domain.created_at
        )

class GradeMapper:
    @staticmethod
    def to_domain(dto: GradeDTO) -> Grade:
        return Grade(
            grade_id=dto.grade_id,
            student_id=dto.student_id,
            course_id=dto.course_id,
            score=dto.score
        )

    @staticmethod
    def to_dto(domain: Grade) -> GradeDTO:
        return GradeDTO(
            grade_id=domain.grade_id,
            student_id=domain.student_id,
            course_id=domain.course_id,
            score=domain.score
        )

class ParentMapper:
    @staticmethod
    def to_domain(dto: ParentDTO) -> Parent:
        return Parent(parent_id=dto.parent_id)

    @staticmethod
    def to_dto(domain: Parent) -> ParentDTO:
        return ParentDTO(parent_id=domain.parent_id)

class CourseMapper:
    @staticmethod
    def to_domain(dto: CourseDTO) -> Course:
        return Course(
            course_id=dto.course_id,
            name=dto.name,
            professor_id=dto.professor_id
        )

    @staticmethod
    def to_dto(domain: Course) -> CourseDTO:
        return CourseDTO(
            course_id=domain.course_id,
            name=domain.name,
            professor_id=domain.professor_id
        )

class StudentMapper:
    @staticmethod
    def to_domain(dto: StudentDTO) -> Student:
        return Student(
            user_id=dto.user_id,
            parent_id=dto.parent_id
        )

    @staticmethod
    def to_dto(domain: Student) -> StudentDTO:
        return StudentDTO(
            user_id=domain.user_id,
            parent_id=domain.parent_id
        )

class AdminMapper:
    @staticmethod
    def to_domain(dto: AdminDTO) -> Admin:
        return Admin(admin_id=dto.admin_id)

    @staticmethod
    def to_dto(domain: Admin) -> AdminDTO:
        return AdminDTO(admin_id=domain.admin_id)

class ProfessorMapper:
    @staticmethod
    def to_domain(dto: ProfessorDTO) -> Professor:
        return Professor(professor_id=dto.professor_id)

    @staticmethod
    def to_dto(domain: Professor) -> ProfessorDTO:
        return ProfessorDTO(professor_id=domain.professor_id)
