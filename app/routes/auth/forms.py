from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Optional,
    Regexp,
    ValidationError,
)

from app.extensions import db
from app.models import User


def _clean_email(value):
    return value.strip().lower() if value else value


def _clean_text(value):
    return value.strip() if value else value


class RegisterForm(FlaskForm):
    full_name = StringField(
        "Nom complet",
        filters=[_clean_text],
        validators=[
            DataRequired("Veuillez saisir votre nom complet."),
            Length(min=2, max=150, message="Le nom doit contenir entre 2 et 150 caractères."),
        ],
    )
    email = StringField(
        "Adresse e-mail",
        filters=[_clean_email],
        validators=[
            DataRequired("Veuillez saisir votre adresse e-mail."),
            Email("Adresse e-mail invalide."),
            Length(max=255),
        ],
    )
    phone = StringField(
        "Téléphone",
        filters=[_clean_text],
        validators=[
            Optional(),
            Length(max=30),
            Regexp(r"^\+?[0-9 ().-]{6,30}$", message="Numéro de téléphone invalide."),
        ],
    )
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired("Veuillez choisir un mot de passe."),
            Length(min=8, max=128, message="Le mot de passe doit contenir au moins 8 caractères."),
        ],
    )
    password_confirm = PasswordField(
        "Confirmer le mot de passe",
        validators=[
            DataRequired("Veuillez confirmer votre mot de passe."),
            EqualTo("password", message="Les deux mots de passe ne correspondent pas."),
        ],
    )

    def validate_email(self, field):
        if db.session.scalar(select(User.id).where(User.email == field.data)):
            raise ValidationError("Un compte existe déjà avec cette adresse e-mail.")

    def validate_phone(self, field):
        if field.data and db.session.scalar(select(User.id).where(User.phone == field.data)):
            raise ValidationError("Ce numéro de téléphone est déjà utilisé.")


class LoginForm(FlaskForm):
    email = StringField(
        "Adresse e-mail",
        filters=[_clean_email],
        validators=[DataRequired("Veuillez saisir votre adresse e-mail.")],
    )
    password = PasswordField(
        "Mot de passe",
        validators=[DataRequired("Veuillez saisir votre mot de passe.")],
    )
    remember = BooleanField("Se souvenir de moi")
