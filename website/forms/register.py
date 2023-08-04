from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import EqualTo, InputRequired, Email, Length
from db.models import User # There is a table of user in my project. You can change it to your table name or delete this import
from .validators import Unique
import email_validator


DATA_EMPTY_MESSAGE = "Обов'язкове до заповнення!"


class RegisterForm(FlaskForm):
    """
    Form for register page.
    """
    username = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=2, max=25)])
    email = EmailField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Email("Невірна пошта!"), Unique(User, "email"), Length(min=5, max=50)])
    password = PasswordField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=8, max=36)])
    password_reply = PasswordField(validators=[EqualTo('password', message="Паролі не співпадають!"), InputRequired(DATA_EMPTY_MESSAGE), Length(min=8, max=36)])
