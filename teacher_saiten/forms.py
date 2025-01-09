from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class PointForm(FlaskForm):
    fieldlist = TextAreaField()
    submit = SubmitField("採点完了")