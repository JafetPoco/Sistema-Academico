#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class profesor_repositorio_impl(Base):
    __tablename__ = 'profesores'

    profesor_id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer)

    # CRUD operations
    def create(self, session, profesor):
        session.add(profesor)
        session.commit()
        return profesor

    def get(self, session, profesor_id):
        return session.query(profesor_repositorio_impl).filter_by(profesor_id=profesor_id).first()

    def update(self, session, profesor_id, **kwargs):
        session.query(profesor_repositorio_impl).filter_by(profesor_id=profesor_id).update(kwargs)
        session.commit()

    def delete(self, session, profesor_id):
        session.query(profesor_repositorio_impl).filter_by(profesor_id=profesor_id).delete()
        session.commit()