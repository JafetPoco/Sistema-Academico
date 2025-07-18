from flask import Blueprint, render_template
from sqlalchemy.orm import Session
from domain.entities import anuncio
from service.mysql import anuncio_repositorio_impl
from app.database import get_session

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')

@anuncios_bp.route('/')
def list_anuncios():
    session: Session = get_session()
    repo = anuncio_repositorio_impl(session)
    anuncios = repo.session.query(anuncio).all()
    return render_template('anuncios/anuncios.html', anuncios=anuncios)
