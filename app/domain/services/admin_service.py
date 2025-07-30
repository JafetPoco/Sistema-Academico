from app.infrastructure.repository.repository import UserRepository
from app.domain.entities import User

class AdminService:
    def __init__(self):
        self.user_repository = UserRepository()

    def update_user(self, user_id: int, role: int):
        user = self.user_repository.get(user_id)
        if user:
            user.role = role
            self.user_repository.update(user.user_id, {'role': role})
            return True
        return False
    
    def get_users(self):
        return self.user_repository.list_all()