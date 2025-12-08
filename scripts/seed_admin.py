import os
from werkzeug.security import generate_password_hash
from app import create_app
from app.domain.entities import Admin, User
from app.domain.services.auth_service import AuthService
from app.infrastructure.repository.repository import UserRepository, AdminRepository

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
ADMIN_NAME = os.getenv("ADMIN_NAME", "Admin User")

app = create_app()

with app.app_context():
    user_repo = UserRepository()
    admin_repo = AdminRepository()

    existing = user_repo.find_by_email(ADMIN_EMAIL)
    if existing:
        print(f"Admin user already exists: {ADMIN_EMAIL}")
    else:
        pwd_hash = generate_password_hash(ADMIN_PASSWORD)
        new_user = User(
            user_id=None,
            full_name=ADMIN_NAME,
            email=ADMIN_EMAIL,
            password_hash=pwd_hash,
            role=AuthService.ADMIN_ROLE,
        )
        created_user, err = user_repo.create(new_user)
        if err:
            raise SystemExit(f"Failed to create admin user: {err}")
        admin_repo.add(Admin(created_user.user_id))
        print(f"Seeded admin user: {ADMIN_EMAIL}")
