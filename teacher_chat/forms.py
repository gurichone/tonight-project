from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class ChatMessageForm(FlaskForm):
    message = TextAreaField(
        "メッセージ",
        validators=[DataRequired(message="メッセージは必須です。"), Length(max=500)],
    )
    submit = SubmitField("送信")