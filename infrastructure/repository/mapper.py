# infrastructure/repository/mapper.py

from domain.entities import *

from infrastructure.repository.models import (
    user_dto,
    announcement_dto,
    grade_dto,
    parent_dto,
    course_dto,
    student_dto,
    admin_dto,
    professor_dto,
)

class UserMapper:
    @staticmethod
    def to_domain(dto: user_dto) -> User:
        return User(
            user_id=dto.user_id,
            full_name=dto.full_name,
            email=dto.email,
            password_hash=dto.password_hash,
            role=dto.role
        )

    @staticmethod
    def to_dto(domain: User) -> user_dto:
        return user_dto(
            user_id=domain.user_id,
            full_name=domain.full_name,
            email=domain.email,
            password_hash=domain.password_hash,
            role=domain.role
        )

class AnnouncementMapper:
    @staticmethod
    def to_domain(dto: announcement_dto) -> Announcement:
        return Announcement(
            announcement_id=dto.announcement_id,
            course_id=dto.course_id,
            user_id=dto.user_id,
            title=dto.title,
            content=dto.content,
            created_at=dto.created_at
        )

    @staticmethod
    def to_dto(domain: Announcement) -> announcement_dto:
        return announcement_dto(
            announcement_id=domain.announcement_id,
            course_id=domain.course_id,
            user_id=domain.user_id,
            title=domain.title,
            content=domain.content,
            created_at=domain.created_at
        )

class GradeMapper:
    @staticmethod
    def to_domain(dto: grade_dto) -> Grade:
        return Grade(
            grade_id=dto.grade_id,
            student_id=dto.student_id,
            course_id=dto.course_id,
            score=dto.score
        )

    @staticmethod
    def to_dto(domain: Grade) -> grade_dto:
        return grade_dto(
            grade_id=domain.grade_id,
            student_id=domain.student_id,
            course_id=domain.course_id,
            score=domain.score
        )

class ParentMapper:
    @staticmethod
    def to_domain(dto: parent_dto) -> Parent:
        return Parent(parent_id=dto.parent_id)

    @staticmethod
    def to_dto(domain: Parent) -> parent_dto:
        return parent_dto(parent_id=domain.parent_id)

class CourseMapper:
    @staticmethod
    def to_domain(dto: course_dto) -> Course:
        return Course(
            course_id=dto.course_id,
            name=dto.name,
            professor_id=dto.professor_id
        )

    @staticmethod
    def to_dto(domain: Course) -> course_dto:
        return course_dto(
            course_id=domain.course_id,
            name=domain.name,
            professor_id=domain.professor_id
        )

class StudentMapper:
    @staticmethod
    def to_domain(dto: student_dto) -> Student:
        return Student(
            user_id=dto.user_id,
            parent_id=dto.parent_id
        )

    @staticmethod
    def to_dto(domain: Student) -> student_dto:
        return student_dto(
            user_id=domain.user_id,
            parent_id=domain.parent_id
        )

class AdminMapper:
    @staticmethod
    def to_domain(dto: admin_dto) -> Admin:
        return Admin(admin_id=dto.admin_id)

    @staticmethod
    def to_dto(domain: Admin) -> admin_dto:
        return admin_dto(admin_id=domain.admin_id)

class ProfessorMapper:
    @staticmethod
    def to_domain(dto: professor_dto) -> Professor:
        return Professor(professor_id=dto.professor_id)

    @staticmethod
    def to_dto(domain: Professor) -> professor_dto:
        return professor_dto(professor_id=domain.professor_id)
