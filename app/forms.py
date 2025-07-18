from flask_wtf import FlaskForm
from flask import Flask
from wtforms import IntegerField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Optional, ValidationError
import app.models as models

class Add_Quest(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField("desc")
    lvl = IntegerField("lvl")
    exp = IntegerField("exp")
    trader = SelectField('trader')
