from flask import render_template
from flask_login import login_required

from app.routes.student import bp


@bp.get("/espace-apprenant")
@login_required
def espace():
    return render_template("espace-apprenant.html")
