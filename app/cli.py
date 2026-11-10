import click
from sqlalchemy import select

from app.extensions import db
from app.models import User
from app.services.roles import DEFAULT_ROLES, ROLE_ADMIN, get_or_create_role


def register_cli(app):
    @app.cli.command("seed-roles")
    def seed_roles():
        """Crée les rôles de base (apprenant, admin)."""
        for name, description in DEFAULT_ROLES.items():
            get_or_create_role(name, description)
        db.session.commit()
        click.echo("Rôles créés : " + ", ".join(DEFAULT_ROLES))

    @app.cli.command("create-admin")
    @click.option("--email", prompt="Adresse e-mail")
    @click.option("--name", "full_name", prompt="Nom complet")
    @click.password_option(confirmation_prompt=True)
    def create_admin(email, full_name, password):
        """Crée un compte administrateur (ou donne le rôle admin à un compte existant)."""
        email = email.strip().lower()
        if len(password) < 8:
            raise click.ClickException("Le mot de passe doit contenir au moins 8 caractères.")

        user = db.session.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(full_name=full_name.strip(), email=email)
            user.set_password(password)
            db.session.add(user)
        admin_role = get_or_create_role(ROLE_ADMIN)
        if admin_role not in user.roles:
            user.roles.append(admin_role)
        db.session.commit()
        click.echo(f"Administrateur prêt : {email}")
