from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField
from wtforms.validators import DataRequired, Optional, ValidationError
import app.models as models

class Add_Quest(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
