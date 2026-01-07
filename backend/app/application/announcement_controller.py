from app.domain.services.announcement_service import AnnouncementService

class AnnouncementController:
    def __init__(self):
        self.service = AnnouncementService()

    @staticmethod
    def _serialize_announcement(announcement):
        if hasattr(announcement, 'to_dict'):
            return announcement.to_dict()
        data = getattr(announcement, '__dict__', {})
        return {k: v for k, v in data.items() if not k.startswith('_')}

    def get_announcements(self, user_id=None, role=0):
        public = self.service.get_public_announcements() or []
        private = []
        if user_id is not None:
            private = self.service.get_private_announcements_for_user(user_id) or []

        return {
            "public_announcements": [self._serialize_announcement(a) for a in public],
            "private_announcements": [self._serialize_announcement(a) for a in private],
            "role": role,
        }

    def create_announcement(self, title: str, content: str, user_id: int, is_private: bool = False, course_id=None):
        if not title or not content:
            return {"success": False, "message": "Título y contenido son obligatorios."}

        created, err = self.service.create_announcement(
            title=title,
            content=content,
            is_private=is_private,
            created_by_user_id=user_id,
            course_id=course_id,
        )

        if err:
            return {"success": False, "message": f"Error al crear el anuncio: {err}"}

        return {
            "success": True,
            "message": "Anuncio creado correctamente.",
            "announcement": self._serialize_announcement(created),
        }
