# app/domain/services/grade_service.py
from app.infrastructure.repository.repository import GradeRepository
from app.infrastructure.repository.repository import CourseRepository
from app.infrastructure.repository.repository import StudentRepository
from app.infrastructure.repository.models import UserDTO  # Asegura que tengas acceso directo al modelo

class GradeService:
    def __init__(self):
        self.grade_repository = GradeRepository()
        self.course_repository = CourseRepository()
        self.student_repository = StudentRepository()

    def get_grades_by_parent_id(self, parent_id):
        students = self.student_repository.get_by_parent_id(parent_id)
        result = []

        for student in students:
            # 🔧 Accedemos al nombre desde la relación con UserDTO
            if hasattr(student, 'user') and student.user:
                full_name = student.user.full_name
            else:
                # 🛠 Fallback en caso la relación no funcione aún
                from app.infrastructure.database import db
                user = db.session.get(UserDTO, student.user_id)
                full_name = user.full_name if user else "Nombre no disponible"

            grades_dto = self.grade_repository.get_by_student_id(student.user_id)
            grades_for_view = []

            for dto in grades_dto:
                course = self.course_repository.get(dto.course_id)
                course_name = course.name if course else "Curso Desconocido"

                grades_for_view.append({
                    'score': dto.score,
                    'course_name': course_name
                })

            result.append({
                'id': student.user_id,
                'name': full_name,
                'grades': grades_for_view
            })

        return result