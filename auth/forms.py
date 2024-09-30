from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

# SignUpFormを作成。フォームを作成する際はとりあえずカッコの中にFlaskFormを書いておく（フォーム作成に必要な機能を使えるようになる）
class SignUpForm(FlaskForm):
    # ユーザネームを入力するフィールドを作成
    username = StringField(  # ユーザネームを入力するフィールドを作成
        "ユーザー名", # フォームに表示される文字を指定
        validators=[
            DataRequired("ユーザ名は必須です。"), # 入力必須の設定
            Length(1, 30, "30文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
    )
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"), # 入力必須の設定
            Email("メールアドレスの形式で入力してください。"), # emailの形式で入力するよう設定
        ],
    )
    password = PasswordField(
        "パスワード", 
        validators=[
            DataRequired("パスワードは必須です。") # 入力必須の設定
        ]
    )
    submit = SubmitField("新規登録") # フォームの入力完了ボタンの作成

# LoginFormを作成。フォームを作成する際はとりあえずカッコの中にFlaskFormを書いておく（フォーム作成に必要な機能を使えるようになる）
class LoginForm(FlaskForm):
    # emailの入力欄を作成
    email = StringField(
        "メールアドレス", # フォームに表示する文字を作成
        validators=[
            DataRequired("メールアドレスは必須です。"), # 入力必須の設定
            Email("メールアドレスの形式で入力してください。"), # メールアドレスの形式で入力するよう設定
        ],
    )
    password = PasswordField("パスワード", validators=[DataRequired("パスワードは必須です。")]) # パスワードを入力必須に設定
    submit = SubmitField("ログイン")