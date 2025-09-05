from flask_wtf import FlaskForm
from flask import Flask
from wtforms import IntegerField, StringField, TextAreaField, SelectField, FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class Add_Quest(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField("desc", validators=[DataRequired()])
    lvl = IntegerField("lvl")
    exp = IntegerField("exp")
    trader = SelectField('trader', validators=[DataRequired()])
    image = FileField("image")
    password = PasswordField("password", validators=[DataRequired()])


class Add_Trader(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField("desc")
    image = FileField("image")
    password = PasswordField("password", validators=[DataRequired()])


class Add_Location(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    desc = TextAreaField("desc")
    image = FileField("image")
    map = FileField("map")
    password = PasswordField("password", validators=[DataRequired()])


class Add_Reward(FlaskForm):
    item = TextAreaField("item", validators=[DataRequired()])
    quest = SelectField("quest", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class Add_Objective(FlaskForm):
    desc = TextAreaField("desc", validators=[DataRequired()])
    quest = SelectField("quest", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class Connect_Location(FlaskForm):
    quest = SelectField("quest", validators=[DataRequired()]) 
    location = SelectField("location", validators=[DataRequired()])   
    password = PasswordField("password", validators=[DataRequired()])


class Connect_Quests(FlaskForm):
    previous = SelectField("previous", validators=[DataRequired()]) 
    subsequent = SelectField("subsequent", validators=[DataRequired()])   
    password = PasswordField("password", validators=[DataRequired()])


class Delete_Quest(FlaskForm):
    quest = SelectField("quest", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class Delete_Trader(FlaskForm):
    trader = SelectField("trader", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class Delete_Location(FlaskForm):
    location = SelectField("location", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


class Searchbar(FlaskForm):
    search = StringField("search")
    submit = SubmitField("submit")
