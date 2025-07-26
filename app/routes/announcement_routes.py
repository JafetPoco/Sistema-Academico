from flask import Blueprint
from app.application.announcement_controller import view_announcements

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')

@anuncios_bp.route('/', methods=['GET'])
def list_all():
    return view_announcements()
