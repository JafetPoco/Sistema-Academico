#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from domain.models.base import Base

class usuario(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True)
    nombres = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    hash_contrasena = Column(String(128), nullable=False)
    rol = Column(Integer, nullable=False)  

    def __init__(self):
        self.usuario_id = None
        self.nombres = None
        self.correo = None
        self.hash_contrasena = None
        self.rol = None

    def cambiar_contrasena(self, nuevo_hash):
        self.hash_contrasena = nuevo_hash
        print("Contraseña cambiada correctamente.")
