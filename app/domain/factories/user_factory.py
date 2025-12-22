from werkzeug.security import generate_password_hash

from app.domain.entities import User


class UserFactory:
    @staticmethod
    def create_with_raw_password(full_name: str, email: str, password: str, role: int) -> User:
        password_hash = generate_password_hash(password)
        return User(
            user_id=None,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role,
        )