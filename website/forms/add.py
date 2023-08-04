from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import InputRequired, Length
from .validators import Unique

from db.processing import Product


DATA_EMPTY_MESSAGE = "Обов'язкове до заповнення!"


class AddForm(FlaskForm):
    image = FileField()
    name = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=2, max=225), Unique(Product, "name")])
    description = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=5, max=1000)])
    size = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=2, max=50)])
    price = IntegerField(validators=[InputRequired(DATA_EMPTY_MESSAGE)])
