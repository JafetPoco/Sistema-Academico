import uuid
from app.domain.entities import Grade

class CalificacionService:
    def __init__(self, calificacion_repo):
        self.calificacion_repo = calificacion_repo

    def calificar_alumno(self, estudiante_id, curso_id, puntaje):
        calificacion = Grade(
            grade_id=str(uuid.uuid4()),
            student_id=estudiante_id,
            course_id=curso_id,
            score=puntaje
        )
        self.calificacion_repo.agregar(calificacion)
        return calificacion

    def ver_calificaciones(self, estudiante_id, calificacion_service):
        return calificacion_service.obtener_calificaciones_por_estudiante(estudiante_id)

    def obtener_calificaciones_por_estudiante(self, estudiante_id):
        return self.calificacion_repo.obtener_por_estudiante(estudiante_id)