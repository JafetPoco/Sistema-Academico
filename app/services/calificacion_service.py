import uuid
from domain.models.Notas.calificacion import Calificacion

class CalificacionService:
    def __init__(self, calificacion_repo):
        self.calificacion_repo = calificacion_repo

    def calificar_alumno(self, estudiante_id, curso_id, puntaje):
        calificacion = Calificacion(
            calificacion_id=str(uuid.uuid4()),
            estudiante_id=estudiante_id,
            curso_id=curso_id,
            puntaje=puntaje
        )
        self.calificacion_repo.agregar(calificacion)
        return calificacion

    def ver_calificaciones(self, estudiante_id, calificacion_service):
        return calificacion_service.obtener_calificaciones_por_estudiante(estudiante_id)

    def obtener_calificaciones_por_estudiante(self, estudiante_id):
        return self.calificacion_repo.obtener_por_estudiante(estudiante_id)