from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, length
from flask_wtf.file import FileAllowed, FileField, FileRequired

class GeminiForms(FlaskForm): #ユーザー新規作成とユーザー編集用のクラスを作成(forms.pyではとりあえずFlaskFormを継承しておく)
    # イベントを入力するフィールドを作成
    question = TextAreaField(
        "問題を入力", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
            # length(max=20, message="20文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
    )
    code = SelectField(
        "ファイルを選択", # フォームに表示される文字を指定
        coerce=int
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成

class JupyterForms(FlaskForm): #ユーザー新規作成とユーザー編集用のクラスを作成(forms.pyではとりあえずFlaskFormを継承しておく)
    # イベントを入力するフィールドを作成
    stdin = TextAreaField(
        "標準入力", # フォームに表示される文字を指定
    )
    stdout = TextAreaField(
        "出力", # フォームに表示される文字を指定
    )
    code = SelectField(
        "ファイルを選択", # フォームに表示される文字を指定
        coerce=int
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成


    # 画像をアップロードするためのフォームの素を作成(とりあえずFlaskFormはかっこの中に書いておく)
class UploadImageForm(FlaskForm):
    code = FileField( # 画像を保存するカラム
        validators=[
            FileRequired("画像ファイルを指定してください。"), # fileの入力必須設定
            FileAllowed(["py"], "サポートされていない画像形式です。"), # png, jpg, jpegファイルのみ受け付ける
        ]
    )
    submit = SubmitField("アップロード")