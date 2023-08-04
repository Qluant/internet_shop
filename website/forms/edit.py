from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.validators import InputRequired, Length


DATA_EMPTY_MESSAGE = "Обов'язкове до заповнення!"


class EditForm(FlaskForm):
    image = FileField()
    name = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=2, max=225)])
    description = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=5, max=1000)])
    size = StringField(validators=[InputRequired(DATA_EMPTY_MESSAGE), Length(min=2, max=50)])
    price = IntegerField(validators=[InputRequired(DATA_EMPTY_MESSAGE)])
