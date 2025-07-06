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
    
    # CRUD operations
    def create(self, session, usuario):
        session.add(usuario)
        session.commit()
        return usuario
    
    def get(self, session, usuario_id):
        return session.query(usuario_repositorio_impl).filter_by(usuario_id=usuario_id).first()
    
    def update(self, session, usuario_id, **kwargs):
        session.query(usuario_repositorio_impl).filter_by(usuario_id=usuario_id).update(kwargs)
        session.commit()
        
    def delete(self, session, usuario_id):
        session.query(usuario_repositorio_impl).filter_by(usuario_id=usuario_id).delete()
        session.commit()