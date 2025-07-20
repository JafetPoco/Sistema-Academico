from app.domain.services.anuncio_service import list_announcements

def get_announcements():
    # validate the list
    announcements = list_announcements()
    if not announcements:
        raise ValueError("No announcements found")
    # return the list of announcements
    return announcements