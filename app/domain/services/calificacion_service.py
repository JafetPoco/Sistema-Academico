import uuid
from app.domain.entities import Grade

class CalificacionService:
    def __init__(self, calificacion_repo):
        self.calificacion_repo = calificacion_repo

    def calificar_alumno(self, grade_data):
        if not (0 <= grade_data['score'] <= 20):
            raise ValueError("La nota debe estar entre 0 y 20")
        
        grade = Grade(
            grade_id=str(uuid.uuid4()),
            student_id=grade_data['student_id'],
            course_id=grade_data['course_id'],
            score=grade_data['score']
        )
        result, error = self.calificacion_repo.add(grade)
        if error:
            raise Exception(f"Error al guardar: {error}")
        return result

    def ver_calificaciones(self, estudiante_id, calificacion_service):
        return calificacion_service.obtener_calificaciones_por_estudiante(estudiante_id)

    def obtener_calificaciones_por_estudiante(self, estudiante_id):
        all_grades = self.calificacion_repo.list_all()
        return [grade for grade in all_grades if grade.student_id == estudiante_id]