from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from app.application.announcement_controller import AnnouncementController

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/api/anuncios')

@anuncios_bp.route('/')
def list_all():
    controller = AnnouncementController()
    public, private, role = controller.get_announcements()

    def _serialize_list(items):
        out = []
        for it in items or []:
            if hasattr(it, 'to_dict'):
                out.append(it.to_dict())
            else:
                data = getattr(it, '__dict__', {})
                out.append({k: v for k, v in data.items() if not k.startswith('_')})
        return out

    return jsonify({
        'public_announcements': _serialize_list(public),
        'private_announcements': _serialize_list(private),
        'role': role
    })


@anuncios_bp.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    role    = session.get("role")
    user_id = session.get("user_id")

    if role != 2 or user_id is None:
        return redirect(url_for('main.index'))

    controller = AnnouncementController()

    if request.method == 'POST':
        msg_type, msg_text = controller.handle_create(request.form, user_id)
        flash(msg_text, msg_type)
        return redirect(url_for('anuncios.admin_panel'))

    return render_template("anuncios/admin_anuncios.html")