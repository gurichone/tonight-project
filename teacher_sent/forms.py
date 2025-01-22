from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DateField, StringField
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileAllowed, FileField, FileRequired


class InformationForms(FlaskForm):
    address = SelectField(
        "宛先",
        choices=[],  # 選択肢は動的に設定
        validators=[
            DataRequired(message="入力は必須です。"),
        ],
    )
    title = TextAreaField(
        "タイトル",
        validators=[
            DataRequired(message="入力は必須です。"),
        ],
    )
    discription = TextAreaField(
        "本文",
        validators=[
            DataRequired(message="本文は必須です。\n本文を入力してください。"),
        ],
    )
    submit = SubmitField("送信")