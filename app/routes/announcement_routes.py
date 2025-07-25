from flask import Blueprint, render_template
from app.application.announcement_controller import get_announcements

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')

@anuncios_bp.route('/')
def list_all():
    announcements = get_announcements()
    return render_template('anuncios/anuncios.html', anuncios=announcements)
