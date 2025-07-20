from app.infrastructure.database import db
from app.infrastructure.repository.repository import AnnouncementRepository

def list_announcements():
    repo = AnnouncementRepository()
    return repo.list_all()