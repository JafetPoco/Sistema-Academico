from flask import Blueprint, render_template 
from app.application.announcement_controller import get_announcements

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')

@anuncios_bp.route('/', methods=['GET'])
def list_all():
    public, private, role = get_announcements()
    return render_template(
        'anuncios/anuncios.html',
        public_announcements=public,
        private_announcements=private,
        role=role
    )
