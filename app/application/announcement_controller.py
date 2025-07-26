from flask import session, render_template
from app.domain.services.announcement_service import AnnouncementService
from app.domain.entities import User

def view_announcements():
    service = AnnouncementService()

    role = session.get('role')
    if role is None:
        user = None
    else:
        user = User(
            user_id=session.get('user_id'),
            email=session.get('email'),
            full_name=session.get('name'),
            role=role,
            password_hash=''
        )

    public_announcements  = service.get_public_announcements()
    private_announcements = service.get_announcements_for_user(user) if user else []

    return render_template(
        'anuncios/anuncios.html',
        public_announcements=public_announcements,
        private_announcements=private_announcements,
        role=role
    )
