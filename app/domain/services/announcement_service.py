from app.domain.entities import Announcement, User
from app.infrastructure.repository.repository import AnnouncementRepository
from typing import List, Optional, Tuple

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
        if not title or not content:
            return None, "Título y contenido son obligatorios."

        announcement = Announcement(
            announcement_id=None,
            course_id=course_id,
            user_id=created_by_user_id,
            title=title.strip(),
            content=content.strip(),
            is_private=is_private,
            created_at=None  # automaticamente se asigna la fecha
        )

        return self.repo.add(announcement)
