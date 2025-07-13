from domain.models.Notas.icalificacion_repositorio import ICalificacionRepositorio
from domain.models.Notas.calificacion import Calificacion

class CalificacionRepositorioImpl(ICalificacionRepositorio):
    def __init__(self, session):
        self.session = session

    def agregar(self, calificacion):
        self.session.add(calificacion)
        self.session.commit()

    def obtener_por_estudiante(self, estudiante_id):
        return self.session.query(Calificacion).filter_by(estudiante_id=estudiante_id).all()