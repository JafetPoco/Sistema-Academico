from app.domain.entities import Announcement, User
from app.infrastructure.repository.repository import AnnouncementRepository
from typing import List

class AnnouncementService:
    def __init__(self):
        self.repo = AnnouncementRepository()

    def get_public_announcements(self) -> List[Announcement]:
        return self.repo.find_public()

    def get_private_announcements_for_user(self, user_id: int) -> List[Announcement]:
        return self.repo.find_private_for_user(user_id)
