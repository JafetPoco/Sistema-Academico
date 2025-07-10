#!/usr/bin/python
# -*- coding: utf-8 -*-

from domain.models.Administrador.ianunciorepositorio import ianuncio_repositorio
from domain.models.Administrador.anuncio import Anuncio

class anuncio_repositorio_impl(ianuncio_repositorio):
    def __init__(self, session):
        self.session = session

    def create(self, anuncio):
        self.session.add(anuncio)
        self.session.commit()

    def get(self, anuncio_id):
        return self.session.query(Anuncio).filter_by(anuncio_id=anuncio_id).first()

    def update(self, anuncio):
        existente = self.session.query(Anuncio).filter_by(anuncio_id=anuncio.anuncio_id).first()
        if existente:
            existente.titulo = anuncio.titulo
            existente.contenido = anuncio.contenido
            existente.curso_id = anuncio.curso_id
            existente.usuario_id = anuncio.usuario_id
            self.session.commit()

    def delete(self, anuncio_id):
        self.session.query(Anuncio).filter_by(anuncio_id=anuncio_id).delete()
        self.session.commit()