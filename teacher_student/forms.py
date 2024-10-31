from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DateTimeField, StringField, ValidationError
from wtforms.validators import DataRequired, Length

class StudentSearch(FlaskForm):
        id = SelectField("生徒番号")

        class_num = SelectField("クラス番号")

        student_name = StringField("氏名")

        submit = SubmitField("検索")
            
            