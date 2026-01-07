from flask import Blueprint, jsonify, request, session
from app.application.announcement_controller import AnnouncementController

anuncios_bp = Blueprint('anuncios', __name__, url_prefix='/api/anuncios')

controller = AnnouncementController()


@anuncios_bp.route('/', methods=['GET'])
def list_all():
    user_id = session.get("user_id")
    role = session.get("role", 0)
    return jsonify(controller.get_announcements(user_id=user_id, role=role))


@anuncios_bp.route('/admin', methods=['POST'])
def admin_panel():
    role = session.get("role")
    user_id = session.get("user_id")

    if role != 2 or user_id is None:
        return jsonify({"success": False, "message": "Acceso no autorizado."}), 403

    title = request.json.get('title') if request.is_json else request.form.get('title')
    content = request.json.get('content') if request.is_json else request.form.get('content')
    is_private = bool(request.json.get('is_private') if request.is_json else request.form.get('is_private'))
    course_id = request.json.get('course_id') if request.is_json else request.form.get('course_id')

    response = controller.create_announcement(
        title=title,
        content=content,
        user_id=user_id,
        is_private=is_private,
        course_id=course_id,
    )
    status_code = 201 if response.get('success') else 400
    return jsonify(response), status_code