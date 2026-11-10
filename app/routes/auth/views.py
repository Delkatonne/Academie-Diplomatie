from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import User
from app.routes.auth import bp
from app.routes.auth.forms import LoginForm, RegisterForm
from app.services.roles import ROLE_STUDENT, get_or_create_role


def _safe_next(target):
    """N'accepte que des chemins internes (évite la redirection vers un site externe)."""
    if (
        target
        and target.startswith("/")
        and not target.startswith("//")
        and "\\" not in target
    ):
        return target
    return None


@bp.route("/inscription", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("student.espace"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data or None,
        )
        user.set_password(form.password.data)
        user.roles.append(get_or_create_role(ROLE_STUDENT))
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            # Compte créé entre-temps avec le même e-mail ou téléphone
            db.session.rollback()
            form.email.errors = list(form.email.errors) + [
                "Cette adresse e-mail ou ce numéro est déjà utilisé."
            ]
            return render_template("inscription.html", form=form), 409

        login_user(user)
        flash("Votre compte a été créé. Bienvenue à l'Académie !", "success")
        return redirect(url_for("student.espace"))

    return render_template("inscription.html", form=form), (400 if form.errors else 200)


@bp.route("/connexion", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("student.espace"))

    form = LoginForm()
    error = None
    if form.validate_on_submit():
        user = db.session.scalar(select(User).where(User.email == form.email.data))
        if user and user.is_active and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(_safe_next(request.args.get("next")) or url_for("student.espace"))
        error = "Adresse e-mail ou mot de passe incorrect."

    status = 401 if error else (400 if form.errors else 200)
    return render_template("connexion.html", form=form, error=error), status


@bp.post("/deconnexion")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "info")
    return redirect(url_for("public.index"))
