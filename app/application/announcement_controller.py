from app.domain.services.announcement_service import AnnouncementService

class AnnouncementController:
    def __init__(self):
        self.service = AnnouncementService()

    def get_announcements(self):
        from flask import session  # imported here to keep controller decoupled

        user_id = session.get("user_id")
        role = session.get("role", 0)

        public = self.service.get_public_announcements()
        private = []

        if user_id is not None:
            private = self.service.get_private_announcements_for_user(user_id)

        return public, private, role

    def handle_create(self, form_data: dict, user_id: int):
        title = form_data.get('title', '').strip()
        content = form_data.get('content', '').strip()
        is_private = bool(form_data.get('is_private'))
        course_id = form_data.get('course_id') or None  # Optional

        if not title or not content:
            return "danger", "Título y contenido son obligatorios."

        created, err = self.service.create_announcement(
            title=title,
            content=content,
            is_private=is_private,
            created_by_user_id=user_id,
            course_id=course_id
        )

        if err:
            return "danger", f"Error al crear el anuncio: {err}"

        return "success", "Anuncio creado correctamente."
