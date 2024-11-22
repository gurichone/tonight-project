from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class AttendCheck(FlaskForm):
    attendance_code = StringField(
        "コード",
        validators=[
            DataRequired("コードを入力してください。"),
            Length(max=6)  # 必要に応じて文字数を変更可能
        ]
    )

    submit = SubmitField("出席登録")