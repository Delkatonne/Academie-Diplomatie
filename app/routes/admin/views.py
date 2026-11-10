from flask import render_template
from sqlalchemy import func, select

from app.extensions import db
from app.models import User
from app.routes.admin import bp
from app.services.roles import ROLE_ADMIN
from app.services.security import roles_required


@bp.get("/")
@roles_required(ROLE_ADMIN)
def dashboard():
    users = db.session.scalars(select(User).order_by(User.created_at.desc())).all()
    total = db.session.scalar(select(func.count(User.id)))
    return render_template("admin-tableau-de-bord.html", users=users, total=total)
