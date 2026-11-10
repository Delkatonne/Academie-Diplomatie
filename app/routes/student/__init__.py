from flask import Blueprint

bp = Blueprint("student", __name__)

from app.routes.student import views  # noqa: E402,F401
