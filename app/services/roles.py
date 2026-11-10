from sqlalchemy import select

from app.extensions import db
from app.models import Role

ROLE_STUDENT = "apprenant"
ROLE_ADMIN = "admin"

DEFAULT_ROLES = {
    ROLE_STUDENT: "Apprenant : accède à son espace et à ses formations",
    ROLE_ADMIN: "Administrateur : gère la plateforme",
}


def get_or_create_role(name, description=None):
    role = db.session.scalar(select(Role).where(Role.name == name))
    if role is None:
        role = Role(name=name, description=description or DEFAULT_ROLES.get(name))
        db.session.add(role)
        db.session.flush()
    return role
