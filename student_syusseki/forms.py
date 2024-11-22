from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import datetime, timedelta
from flask import session

class AttendCheck(FlaskForm):
    attendance_code = StringField(
        "コード",
        validators=[
            DataRequired("コードを入力してください。"),
            Length(max=6, message="コードは6文字以内で入力してください。")
        ]
    )
    submit = SubmitField("出席登録")

    def validate_attendance_code(self, field):
        saved_code = session.get("attendance_code")
        code_timestamp = session.get("code_timestamp")
        
        # コードが発行されていない場合のエラーメッセージ
        if not saved_code or not code_timestamp:
            raise ValidationError("有効なコードが発行されていません。")
        
        # コードの有効期限（1分）が切れている場合のエラーメッセージ
        issue_time = datetime.fromtimestamp(code_timestamp)
        if datetime.now() > issue_time + timedelta(minutes=1):
            raise ValidationError("出席コードの有効期限が切れています。")
        
        # 入力されたコードが一致しない場合のエラーメッセージ
        if field.data != saved_code:
            raise ValidationError("コードが一致しません。")
