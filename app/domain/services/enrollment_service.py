# app/domain/services/enrollment_service.py
from app.infrastructure.repository.repository import EnrollmentRepository, UserRepository, CourseRepository

class EnrollmentService:
    def __init__(self):
        self.enrollment_repo = EnrollmentRepository()
        self.user_repo = UserRepository()
        self.course_repo = CourseRepository()

    def get_students_enrolled_in_course(self, course_id: int):
        try:
            students_data, error = self.enrollment_repo.get_course_students_with_names(course_id)
            if error:
                return [], error
            
            # Formatear datos para el frontend
            students = []
            for student in students_data:
                students.append({
                    'id': student['id'],
                    'name': student['name']
                })
            
            return students, None
            
        except Exception as e:
            return [], f"Error obteniendo estudiantes: {str(e)}"

    def get_professor_courses(self, professor_id: int):
        try:
            courses, error = self.course_repo.get_courses_by_professor(professor_id)
            if error:
                return [], error
            
            return courses, None
            
        except Exception as e:
            return [], f"Error obteniendo cursos del profesor: {str(e)}"

    def validate_professor_course_access(self, professor_id: int, course_id: int):
        try:
            courses, error = self.get_professor_courses(professor_id)
            if error:
                return False, error
            
            course_ids = [course['id'] for course in courses]
            if course_id not in course_ids:
                return False, "No tienes permisos para calificar estudiantes de este curso"
            
            return True, None
            
        except Exception as e:
            return False, f"Error validando acceso: {str(e)}"
        
    def get_count_students_enrollment(self, course_id: int):
        count_students = self.enrollment_repo.count_students_by_course(course_id)
        return count_students
    
    def get_professor_courses_with_student_counts(self, professor_id: int):
        try:
            courses, error = self.get_professor_courses(professor_id)
            if error:
                return [], error
            
            course_with_counts = []
            for course in courses:
                count = self.get_count_students_enrollment(course['id'])
                course_with_counts.append({
                    'id': course['id'],
                    'nombre': course['name'],
                    'student_count': count
                })
            
            return course_with_counts, None
        
        except Exception as e:
            return [], f"Error al obtener cursos con conteo de estudiantes: {str(e)}"
