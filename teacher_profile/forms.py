from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class ProfileImageForm(FlaskForm):
    profile_image = FileField('画像を選択', validators=[
        DataRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png'], '画像ファイルのみアップロードできます。')
    ])
    submit = SubmitField('編集完了')

class PasswordResetForm(FlaskForm):
    oldpassword = PasswordField(
        "現在のパスワード",
        validators=[
            DataRequired("このフィールドを入力してください") # 入力必須の設定
        ],
    )
    password1 = PasswordField(
        "新しいパスワード",
        validators=[
            DataRequired("このフィールドを入力してください") # 入力必須の設定
        ],
    )
    password2 = PasswordField(
        "再確認",
        validators=[
            DataRequired("このフィールドを入力してください") # 入力必須の設定
        ],
    )
    submit = SubmitField('決定')