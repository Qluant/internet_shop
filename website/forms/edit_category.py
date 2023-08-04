from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length


DATA_EMPTY_MESSAGE = "Обов'язкове до заповнення!"


class CategoryEditForm(FlaskForm):
    title = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=2, max=225)])
    description = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=5, max=1000)])
