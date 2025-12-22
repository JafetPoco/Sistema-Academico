"""
User Factory for creating User domain objects.

This factory handles the creation of User entities, including password hashing
and validation logic, following the Factory Method design pattern.
"""
from werkzeug.security import generate_password_hash
from app.domain.entities import User
from app.domain.roles import Role


class UserFactory:
    """
    Factory for creating User domain entities.
    
    Handles creation logic including password hashing and role initialization.
    Follows the Factory Method design pattern.
    """
    
    @staticmethod
    def create_with_raw_password(full_name: str, email: str, password: str, 
                                 role: int = 0) -> User:
        """
        Create a User entity with a raw password (will be hashed).
        
        Args:
            full_name: User's full name
            email: User's email address
            password: Raw password (will be hashed)
            role: User role (use Role enum values). Defaults to UNKNOWN (0)
            
        Returns:
            User domain entity with hashed password
        """
        password_hash = generate_password_hash(password)
        return User(
            user_id=None,  # Will be set by repository
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role
        )
    
    @staticmethod
    def create_with_hash(user_id: int, full_name: str, email: str, 
                        password_hash: str, role: int) -> User:
        """
        Create a User entity with a pre-hashed password.
        
        Useful when loading users from database or for testing.
        
        Args:
            user_id: User's unique identifier
            full_name: User's full name
            email: User's email address
            password_hash: Already hashed password
            role: User role (use Role enum values)
            
        Returns:
            User domain entity
        """
        return User(
            user_id=user_id,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role=role
        )
    
    @staticmethod
    def create_teacher(user_id: int, full_name: str, email: str, 
                      password_hash: str) -> User:
        """
        Create a teacher User entity.
        
        Args:
            user_id: User's unique identifier
            full_name: User's full name
            email: User's email address
            password_hash: Already hashed password
            
        Returns:
            User domain entity with TEACHER role
        """
        return UserFactory.create_with_hash(user_id, full_name, email, password_hash, Role.TEACHER)
    
    @staticmethod
    def create_parent(user_id: int, full_name: str, email: str, 
                     password_hash: str) -> User:
        """
        Create a parent User entity.
        
        Args:
            user_id: User's unique identifier
            full_name: User's full name
            email: User's email address
            password_hash: Already hashed password
            
        Returns:
            User domain entity with PARENT role
        """
        return UserFactory.create_with_hash(user_id, full_name, email, password_hash, Role.PARENT)
    
    @staticmethod
    def create_admin(user_id: int, full_name: str, email: str, 
                    password_hash: str) -> User:
        """
        Create an admin User entity.
        
        Args:
            user_id: User's unique identifier
            full_name: User's full name
            email: User's email address
            password_hash: Already hashed password
            
        Returns:
            User domain entity with ADMIN role
        """
        return UserFactory.create_with_hash(user_id, full_name, email, password_hash, Role.ADMIN)
