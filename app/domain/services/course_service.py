# app/domain/services/course_service.py
class CourseService:
    def __init__(self, course_repository):
        self.course_repository = course_repository
    
    def get_courses_by_professor(self, professor_id):
        try:
            if not professor_id or professor_id <= 0:
                raise ValueError("ID de profesor inválido")
            
            courses_data, error = self.course_repository.get_courses_by_professor(professor_id)
            
            if error:
                raise RuntimeError(error)
            
            # Aplicar validaciones de dominio
            valid_courses = [
                course for course in courses_data 
                if course.get('name') and course['name'].strip()
            ]
            
            return valid_courses
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Error obteniendo cursos del profesor: {str(e)}")
    
    def get_all_courses(self):
        try:
            courses_data, error = self.course_repository.get_all_courses()
            
            if error:
                raise RuntimeError(error)
            
            return courses_data
            
        except Exception as e:
            raise RuntimeError(f"Error obteniendo cursos: {str(e)}")