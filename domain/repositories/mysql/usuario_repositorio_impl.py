#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class usuario_repositorio_impl(Base):
    __tablename__ = 'usuarios'

    usuario_id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    apellido = Column(String(100))
    correo = Column(String(100))
    hash_contraseña = Column(String(256))