import uuid
from domain.models.Notas.Calificacion import calificacion

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