from app.domain.services.anuncio_service import listall_announcements

def get_announcements():
    announcements = listall_announcements()
    return announcements
