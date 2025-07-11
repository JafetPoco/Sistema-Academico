from domain.models.Notas.icalificacion_repositorio import ICalificacionRepositorio

class CalificacionRepositorioImpl(ICalificacionRepositorio):
    def __init__(self, session):
        self.session = session

    def agregar(self, calificacion):
        self.session.add(calificacion)
        self.session.commit()