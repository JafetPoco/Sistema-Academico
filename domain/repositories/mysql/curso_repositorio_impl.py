#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class curso_repositorio_impl(Base):
    __tablename__ = 'cursos'

    curso_id = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    Attribute1 = Column(String(100))

    # CRUD operations
    def create(self, session, curso):
        session.add(curso)
        session.commit()
        return curso

    def get(self, session, curso_id):
        return session.query(curso_repositorio_impl).filter_by(curso_id=curso_id).first()

    def update(self, session, curso_id, **kwargs):
        session.query(curso_repositorio_impl).filter_by(curso_id=curso_id).update(kwargs)
        session.commit()

    def delete(self, session, curso_id):
        session.query(curso_repositorio_impl).filter_by(curso_id=curso_id).delete()
        session.commit()