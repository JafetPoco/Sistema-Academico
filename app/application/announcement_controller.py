from flask import session, render_template
from app.domain.services.announcement_service import AnnouncementService

def get_announcements():
    service = AnnouncementService()

    user_id = session.get("user_id")
    role = session.get("role", 0)

    public = service.get_public_announcements()
    private = []

    if user_id is not None:
        private = service.get_private_announcements_for_user(user_id)

    return public, private, role
