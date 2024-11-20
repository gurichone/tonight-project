from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, length

class AttendCheck(FlaskForm):
    attend_code = StringField(
        "コード",
        validators=[
            DataRequired("コードを入力してください。")
        ]
    )

    submit = SubmitField("出席登録")