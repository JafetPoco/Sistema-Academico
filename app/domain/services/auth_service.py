from werkzeug.security import generate_password_hash, check_password_hash
from app.infrastructure.repository.repository import UserRepository
from app.domain.entities import User

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def is_email_taken(self, email):
        return self.user_repo.find_by_email(email) is not None

    def register_user(self, full_name: str, email: str, password: str, role: int = 0):
        if self.is_email_taken(email):
            return {"status": "error", "message": "Ya existe un usuario con este correo"}

        password_hash = generate_password_hash(password)
        new_user = User(
            user_id=None,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role
        )

        created_user, err = self.user_repo.create(new_user)
        if err:
            return {"status": "error", "message": err}

        return {"status": "success", "user": created_user}
    
    def authenticate(self, email: str, password: str) -> dict:
        user = self.user_repo.find_by_email(email)
        if not user:
            return {"status": "error", "message": "Usuario no registrado"}

        if user.role == 0:
            return {"status": "error", "message": "Aun no se activo su cuenta, contáctese con un administrador si cree que esto se trata de un error."}

        if not check_password_hash(user.password_hash, password):
            return {"status": "error", "message": "Contraseña incorrecta"}

        return {"status": "success", "user": user}

    def validate_registration_data(self, full_name, email, password, confirm):
        if not full_name or not email or not password or not confirm:
            return {"status": "error", "message": "Todos los campos son obligatorios."}
        
        if password != confirm:
            return {"status": "error", "message": "Las contraseñas no coinciden."}
        
        return {"status": "success"}
