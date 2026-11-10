from pathlib import Path

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from config import Config
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_class=Config):
    frontend_dir = Path(__file__).resolve().parent.parent / "frontend"

    # Les pages HTML du dossier frontend/ sont des modèles Jinja.
    # static_folder=None : seuls css/, js/ et images/ sont servis (voir routes/public).
    app = Flask(
        __name__,
        template_folder=str(frontend_dir),
        static_folder=None,
    )

    app.config.from_object(config_class)
    app.config["FRONTEND_DIR"] = frontend_dir

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY manquante : renseignez-la dans le fichier .env "
            "(voir .env.example)."
        )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
    login_manager.login_message_category = "info"

    # Importer les modèles afin que Flask-Migrate les détecte.
    from app import models  # noqa: F401

    from app.routes.public import bp as public_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.student import bp as student_bp
    from app.routes.admin import bp as admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)

    from app.cli import register_cli

    register_cli(app)

    return app


def register_error_handlers(app):
    def render_error(code, title, message):
        return render_template(
            "erreur.html", code=code, title=title, message=message
        ), code

    @app.errorhandler(403)
    def forbidden(_e):
        return render_error(403, "Accès refusé", "Vous n'avez pas l'autorisation d'accéder à cette page.")

    @app.errorhandler(404)
    def not_found(_e):
        return render_error(404, "Page introuvable", "La page que vous cherchez n'existe pas ou a été déplacée.")

    @app.errorhandler(CSRFError)
    def csrf_error(_e):
        return render_error(400, "Session expirée", "Votre formulaire a expiré. Rechargez la page et réessayez.")

    @app.errorhandler(500)
    def server_error(_e):
        db.session.rollback()
        return render_error(500, "Erreur du serveur", "Une erreur est survenue. Réessayez dans un instant.")
