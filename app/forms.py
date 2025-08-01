from flask_wtf import FlaskForm
from flask import Flask
from wtforms import IntegerField, StringField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Optional, ValidationError

class Add_Quest(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField("desc")
    lvl = IntegerField("lvl")
    exp = IntegerField("exp")
    trader = SelectField('trader')

class Add_Trader(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField("desc")
    image = FileField("image")

class Add_Location(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField("desc")
