from app.infrastructure.repository.repository import AnnouncementRepository

def listall_announcements():
    repo = AnnouncementRepository()
    return repo.list_all()
