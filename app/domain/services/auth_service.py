from werkzeug.security import generate_password_hash, check_password_hash
from app.infrastructure.repository.repository import UserRepository
from app.domain.entities import User

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, full_name: str, email: str, password: str, role: int = 0):
        existing = self.user_repo.find_by_email(email)
        if existing:
            return None, "Ya existe un usuario con este correo."

        password_hash = generate_password_hash(password)
        new_user = User(
            user_id=None,  # se autogenera
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role
        )
        created_user, err = self.user_repo.create(new_user)
        if err:
            return None, err
        return created_user, None
    
    def authenticate(self, email: str, password: str):
        user = self.user_repo.find_by_email(email)
        if not user:
            return None
        if check_password_hash(user.password_hash, password):
            return user
        return None

    def validate_registration_data(self,full_name, email, password, confirm):
        if not full_name or not email or not password or not confirm:
            return False, "Todos los campos son obligatorios."
        if password != confirm:
            return False, "Las contraseñas no coinciden."
        return True, None
