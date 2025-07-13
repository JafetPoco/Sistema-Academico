#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String,ForeignKey
from sql.alchemy.orm import relationship
from models.base import Base

class curso(Base):

    __tablename__ = 'cursos'
    curso_id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    profesor_id = Column(Integer, ForeignKey('profesores.profesor_id'), nullable=False)

    profesor = relationship("profesor", back_populates="cursos")

    def agregar_estudiante(self, estudiante):
        pass

    def calcular_promedio(self, ):
        pass
