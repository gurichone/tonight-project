from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta
from flask import session
from app import db
from teacher_seiseki.models import Score
from auth.models import Subject

class AttendCheck(FlaskForm):
    attendance_code = StringField(
        "コード",
        validators=[
            DataRequired("コードを入力してください。"),
            Length(max=6, message="コードは6文字以内で入力してください。")
        ]
    )
    submit = SubmitField("出席登録")

    