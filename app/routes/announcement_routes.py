from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app.application.announcement_controller import AnnouncementController
from app.domain.roles import Role

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/anuncios')


@anuncios_bp.route('/', methods=['GET'])
def list_all():
    controller = AnnouncementController()
    public, private, role = controller.get_announcements()
    return render_template(
        'anuncios/anuncios.html',
        public_announcements=public,
        private_announcements=private,
        role=role
    )


@anuncios_bp.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    """Admin panel for managing announcements. Restricted to administrators."""
    user_role = session.get("role")
    user_id = session.get("user_id")

    # Only admins can access this panel
    if user_role != Role.ADMIN or user_id is None:
        return redirect(url_for('main.index'))

        return redirect(url_for('main.index'))

        return redirect(url_for('main.index'))

        return redirect(url_for('main.index'))

    controller = AnnouncementController()

    if request.method == 'POST':
        msg_type, msg_text = controller.handle_create(request.form, user_id)
        flash(msg_text, msg_type)
        return redirect(url_for('anuncios.admin_panel'))

    return render_template("anuncios/admin_anuncios.html")
