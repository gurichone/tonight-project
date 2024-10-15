from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length
class EventForm(FlaskForm): #ユーザー新規作成とユーザー編集用のクラスを作成(forms.pyではとりあえずFlaskFormを継承しておく)
    # イベントを入力するフィールドを作成
    event = StringField(
        "イベント名", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="イベント名は必須です。"),  # 入力必須の設定
            length(max=20, message="20文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
    )
    date = DateField(
        "日付", # フォームに表示する文字を指定
            validators=[
                DataRequired(message="日付は必須です。"),  # 入力必須の設定
            ],
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成