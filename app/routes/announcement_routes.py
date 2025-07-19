from flask import Blueprint, render_template
from app.application.announcement_controller import 

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')

@anuncios_bp.route('/')
def list_anuncios():
    session: Session = get_session()
    repo = anuncio_repositorio_impl(session)
    anuncios = repo.session.query(anuncio).all()
    return render_template('anuncios/anuncios.html', anuncios=anuncios)
