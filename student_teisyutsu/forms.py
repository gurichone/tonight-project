#gvuihbjhgvhuygibjhvyuihjkbh
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileAllowed, FileField, FileRequired


class SubmitForms(FlaskForm): #ユーザー新規作成とユーザー編集用のクラスを作成(forms.pyではとりあえずFlaskFormを継承しておく)
    # イベントを入力するフィールドを作成
    file = FileField(
        "ファイルを選択", # フォームに表示される文字を指定
        validators=[
            FileRequired("ファイルを指定してください。"), # fileの入力必須設定
            FileAllowed(["py", "java", "txt", "html", "zip"], "サポートされていない画像形式です。"), # png, jpg, jpegファイルのみ受け付ける
        ]
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成