from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, length
class GeminiForms(FlaskForm): #ユーザー新規作成とユーザー編集用のクラスを作成(forms.pyではとりあえずFlaskFormを継承しておく)
    # イベントを入力するフィールドを作成
    question = TextAreaField(
        "問題を入力", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
            # length(max=20, message="20文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
    )
    code = TextAreaField(
        "コードを入力", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
            # length(max=20, message="20文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成