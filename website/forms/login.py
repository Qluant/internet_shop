from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField
from wtforms.validators import InputRequired
from db.models import User # There is a table of user in my project. You can change it to your table name or delete this import
from .validators import AuthorizationEmail, AuthorizationPassword


DATA_EMPTY_MESSAGE = "Заповніть це поле!"


class LoginForm(FlaskForm):
    """ 
    Form for login page.
    """
    email = EmailField(validators=[InputRequired(DATA_EMPTY_MESSAGE), AuthorizationEmail(User)])
    password = PasswordField(validators=[InputRequired(DATA_EMPTY_MESSAGE), AuthorizationPassword(User)])
