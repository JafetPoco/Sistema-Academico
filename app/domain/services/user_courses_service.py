from app.infrastructure.repository.repository import UserRepository
from app.infrastructure.repository.repository import CourseRepository
from app.infrastructure.repository.repository import StudentRepository
from app.infrastructure.repository.repository import GradeRepository
from app.domain.entities import User
from sqlalchemy.exc import SQLAlchemyError

class UserCoursesService:
    def __init__(self):
        self.user_repository= UserRepository()
        self.course_repository= CourseRepository()
        self.student_repository= StudentRepository()
        self.grade_repository= GradeRepository()

    def get_student_by_parent_id(self, parent_id):
        students = self.student_repository.get_by_parent_id(parent_id)
        results = []
        for student in students:
            results.append(student.user_id)
        return results
   
    def get_courses_by_student_id(self, student_id):

        # 1) Obtener todas las calificaciones
        try:
            grades = self.grade_repository.get_by_student_id(student_id)
        except SQLAlchemyError:
            return []

        # 2) Extraer todos los IDs (puede haber duplicados)
        course_ids = [g.course_id for g in grades]
        if not course_ids:
            return []

        # 3) Recuperar todos los nombres en un solo query
        id_to_name = self.course_repository.get_names_by_ids(course_ids)
        print(f"DEBUG: id_to_name map: {id_to_name}")

        # 4) Construir resultados, preservando duplicados si quieres
        results = []
        for cid in course_ids:
            name = id_to_name.get(cid)
            if name:
                results.append({'course_id': cid, 'course_name': name})
        print(f"DEBUG: resultados finales para student_id {student_id}: {results}")
        
        return results