from app.domain.entities import Announcement
from app.infrastructure.repository.repository import AnnouncementRepository
from typing import List, Optional, Tuple, Dict
import logging

class AnnouncementService:
    def __init__(self):
        self.repo = AnnouncementRepository()

    def get_public_announcements(self) -> List[Announcement]:
        return self.repo.find_public()

    def get_private_announcements_for_user(self, user_id: int) -> List[Announcement]:
        return self.repo.find_private_for_user(user_id)

    def create_announcement(
        self,
        title: str,
        content: str,
        is_private: bool,
        created_by_user_id: int,
        course_id: Optional[int] = None
    ) -> Tuple[Optional[Announcement], Optional[str]]:
        title = (title or "").strip()
        content = (content or "").strip()

        if not title or not content:
            return None, "Título y contenido son obligatorios."

        if created_by_user_id is None:
            return None, "ID de usuario inválido."

        if course_id:
            try:
                course_id = int(course_id)
            except ValueError:
                return None, "ID de curso inválido."

        announcement = Announcement(
            announcement_id=None,
            course_id=course_id,
            user_id=created_by_user_id,
            title=title,
            content=content,
            is_private=bool(is_private),
            created_at=None
        )

        return self.repo.add(announcement)

