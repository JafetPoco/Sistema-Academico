#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from domain.models.base import Base

class estudiante(Base):

    __tablename__ = 'estudiantes'
    id = Column(Integer, ForeignKey('usuarios.usuario_id'), primary_key=True)
    padre_id = Column(Integer, ForeignKey('padres.id'), nullable=True)

    padre = relationship("padre", back_populates="estudiantes")
    
    def agregar_padre(self, padre):

        if not isinstance(padre, padre):
            raise ValueError("El objeto proporcionado no es un padre válido.")
        self.padre_id = padre.id
