from app.infrastructure.repository.repository import StudentRepository

class StudentService:
    def __init__(self, student_repository):
        self.student_repository = student_repository
    
    def get_all_students(self):
        try:
            students = self.student_repository.list_all()
            return students
        except Exception as e:
            raise RuntimeError(f"Error al obtener estudiantes: {str(e)}")
    
    def obtener_estudiante_por_id(self, student_id):
        try:
            return self.student_repository.get(student_id)
        except Exception as e:
            raise RuntimeError(f"Error al obtener estudiante: {str(e)}")