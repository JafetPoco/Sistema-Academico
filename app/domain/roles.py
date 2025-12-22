"""
Domain module for role management and permissions.

This module centralizes all role-related definitions and provides
a single source of truth for role constants and role-based operations.
"""
from enum import IntEnum
from typing import List, Set


class Role(IntEnum):
    """Enumeration of user roles in the academic system."""
    UNKNOWN = 0
    TEACHER = 1
    ADMIN = 2
    PARENT = 3

    @classmethod
    def is_valid(cls, role: int) -> bool:
        """Check if a role value is valid."""
        return role in [r.value for r in cls]

    @classmethod
    def from_int(cls, role_int: int) -> 'Role':
        """Convert integer to Role enum with validation."""
        if not cls.is_valid(role_int):
            return cls.UNKNOWN
        return cls(role_int)


class RoleHierarchy:
    """Defines the hierarchy and relationships between roles."""
    
    # Roles that can view grades
    CAN_VIEW_GRADES = {Role.PARENT, Role.TEACHER, Role.ADMIN}
    
    # Roles that can assign grades
    CAN_ASSIGN_GRADES = {Role.TEACHER, Role.ADMIN}
    
    # Roles that can manage users
    CAN_MANAGE_USERS = {Role.ADMIN}
    
    # Roles that can manage courses
    CAN_MANAGE_COURSES = {Role.TEACHER, Role.ADMIN}
    
    # Roles that can manage announcements
    CAN_MANAGE_ANNOUNCEMENTS = {Role.ADMIN}
    
    # Roles that can view reports
    CAN_VIEW_REPORTS = {Role.TEACHER, Role.ADMIN, Role.PARENT}


class RolePermissions:
    """Maps roles to their permissions."""
    
    PERMISSIONS_MAP = {
        Role.UNKNOWN: ["view_grades", "view_profile"],
        Role.TEACHER: ["qualify_students", "view_courses", "view_reports", "manage_grades"],
        Role.PARENT: ["view_children", "view_messages", "view_grades"],
        Role.ADMIN: ["manage_users", "manage_courses", "view_all_reports", "manage_system"],
    }
    
    ROLE_DISPLAY_NAMES = {
        Role.UNKNOWN: "Unknown",
        Role.TEACHER: "Profesor",
        Role.PARENT: "Padre",
        Role.ADMIN: "Administrador",
    }
    
    @classmethod
    def get_permissions(cls, role: Role) -> List[str]:
        """Get the list of permissions for a given role."""
        if isinstance(role, int):
            role = Role.from_int(role)
        return cls.PERMISSIONS_MAP.get(role, [])
    
    @classmethod
    def get_display_name(cls, role: Role) -> str:
        """Get the display name for a role."""
        if isinstance(role, int):
            role = Role.from_int(role)
        return cls.ROLE_DISPLAY_NAMES.get(role, "Usuario")
    
    @classmethod
    def has_permission(cls, role: Role, permission: str) -> bool:
        """Check if a role has a specific permission."""
        if isinstance(role, int):
            role = Role.from_int(role)
        permissions = cls.get_permissions(role)
        return permission in permissions
    
    @classmethod
    def can_access_qualification(cls, role: Role) -> bool:
        """Check if a role can access the qualification system."""
        if isinstance(role, int):
            role = Role.from_int(role)
        return role in RoleHierarchy.CAN_ASSIGN_GRADES
    
    @classmethod
    def is_admin(cls, role: Role) -> bool:
        """Check if a role is an administrator."""
        if isinstance(role, int):
            role = Role.from_int(role)
        return role == Role.ADMIN
    
    @classmethod
    def is_teacher(cls, role: Role) -> bool:
        """Check if a role is a teacher."""
        if isinstance(role, int):
            role = Role.from_int(role)
        return role == Role.TEACHER
    
    @classmethod
    def is_parent(cls, role: Role) -> bool:
        """Check if a role is a parent."""
        if isinstance(role, int):
            role = Role.from_int(role)
        return role == Role.PARENT
    
    @classmethod
    def is_teacher_or_admin(cls, role: Role) -> bool:
        """Check if a role is either teacher or admin."""
        if isinstance(role, int):
            role = Role.from_int(role)
        return role in {Role.TEACHER, Role.ADMIN}
