# app/domain/services/grade_service.py
from typing import Optional

from app.infrastructure.repository.repository import GradeRepository
from app.infrastructure.repository.repository import CourseRepository
from app.infrastructure.repository.repository import StudentRepository
from app.infrastructure.repository.models import UserDTO  # Asegura que tengas acceso directo al modelo

class GradeService:
    def __init__(
        self,
        grade_repository: Optional[GradeRepository] = None,
        course_repository: Optional[CourseRepository] = None,
        student_repository: Optional[StudentRepository] = None,
    ):
        # Allow dependency injection to simplify testing without touching the DB
        self.grade_repository = grade_repository or GradeRepository()
        self.course_repository = course_repository or CourseRepository()
        self.student_repository = student_repository or StudentRepository()

    def get_grades_by_parent_id(self, parent_id):
        students = self.student_repository.get_by_parent_id(parent_id)
        return [self._build_student_result(student) for student in students]

    def _build_student_result(self, student):
        return {
            'id': student.user_id,
            'name': self._resolve_student_name(student),
            'grades': self._build_grades_for_view(student.user_id),
        }

    def _build_grades_for_view(self, student_id):
        return [self._map_grade(dto) for dto in self.grade_repository.get_by_student_id(student_id)]

    def _map_grade(self, dto):
        course = self.course_repository.get(dto.course_id)
        course_name = course.name if course else "Curso Desconocido"

        return {
            'score': dto.score,
            'course_name': course_name,
        }

    def _resolve_student_name(self, student):
        if hasattr(student, 'user') and student.user:
            return student.user.full_name

        from app.infrastructure.database import db

        user = db.session.get(UserDTO, student.user_id)
        return user.full_name if user else "Nombre no disponible"