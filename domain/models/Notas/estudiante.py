#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, ForeignKey
from domain.models.base import Base

class estudiante(Base):

    tablename = 'estudiantes'
    id = Column(Integer, ForeignKey('usuarios.usuario_id'), primary_key=True)
    padre_id = Column(Integer, ForeignKey('padres.id'), nullable=True)
    
    def __init__(self):
        self.estudiante_id = None
        self.usuario_id = None
