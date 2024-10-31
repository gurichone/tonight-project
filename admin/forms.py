from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class CourseForm(FlaskForm):
    course_name = StringField(
        "コース名",
        validators=[
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )
    submit = SubmitField("登録")

class SubjectForm(FlaskForm):
    subject_name = StringField(
        "科目名",
        validators=[
            Length(1, 20, "20文字以内で入力してください。"),
        ],
    )
    submit = SubmitField("登録")

class ClassNumForm(FlaskForm):
    class_num = StringField(
        "クラス番号",
        validators=[
            Length(4, 4, "4文字で入力してください。"),
        ],
    )
    course = SelectField(
        "コース名",
    )
    submit = SubmitField("登録")

class CourseSubjectForm(FlaskForm):
    course = SelectField(
        "コース名",
    )
    subject = SelectField(
        "科目名"
    )
    submit = SubmitField("登録")