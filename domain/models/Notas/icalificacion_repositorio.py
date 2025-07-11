from abc import ABC, abstractmethod

class ICalificacionRepositorio(ABC):
    @abstractmethod
    def agregar(self, calificacion):
        pass