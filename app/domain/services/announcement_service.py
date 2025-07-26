from app.domain.entities import Announcement, User
from app.infrastructure.repository.repository import AnnouncementRepository
from typing import List

class AnnouncementService:
    def __init__(self):
        self.announcement_repo = AnnouncementRepository() 

    def get_public_announcements(self) -> List[Announcement]:
        return [
            anuncio for anuncio in self.announcement_repo.list_all()
            if not anuncio.is_private
        ]

    def get_announcements_for_user(self, user: User) -> List[Announcement]:
        all_announcements = self.announcement_repo.list_all()

        # Admin ve todo (incluidos privados)
        if user.role == 2:
            return [a for a in all_announcements]

        # Estudiante o profesor ve solo públicos + privados de sus cursos (si se aplica)
        return [
            a for a in all_announcements
            if not a.is_private or a.user_id == user.user_id
        ]
