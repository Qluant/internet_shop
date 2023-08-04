from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from .validators import Unique

from db.processing import Category


DATA_EMPTY_MESSAGE = "Обов'язкове до заповнення!"


class CategoryAddForm(FlaskForm):
    title = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=2, max=225), Unique(Category, "title")])
    description = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=5, max=1000)])
