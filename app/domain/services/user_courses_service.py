from app.infrastructure.repository.repository import UserRepository
from app.infrastructure.repository.repository import CourseRepository
from app.infrastructure.repository.repository import StudentRepository
from app.infrastructure.repository.repository import GradeRepository
from app.domain.entities import User

class UserCoursesService:
    def __init__(self):
        self.user_repository= UserRepository()
        self.course_repository= CourseRepository()
        self.student_repository= StudentRepository()
    def get_student_by_parent_id(self, parent_id):
        students = self.student_repository.get_by_parent_id(parent_id)
        result = []
        if hasattr(student, 'user') and student.user:
            full_name = student.user.full_name
        else:
            # Fallback
            from app.infrastructure.database import db
            user = db.session.get(UserDTO, student.user_id)
            full_name = user.full_name if user else "Nombre no disponible"
            
    def get_courses_by_student_id(self, student_id):
        pass