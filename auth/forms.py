from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, Length, NumberRange

# SignUpFormを作成。フォームを作成する際はとりあえずカッコの中にFlaskFormを書いておく（フォーム作成に必要な機能を使えるようになる）
class TeacherSignUpForm(FlaskForm):
    teacher_id = StringField(
        "教員番号",
        validators=[
            DataRequired("教員番号は必須です。"), # 入力必須の設定
            Length(6, 6, "6文字で入力してください。"), # 教員番号は6桁
        ],
        render_kw={"placeholder": "教員番号"}
    )
    teacher_name = StringField(  # ユーザネームを入力するフィールドを作成
        "氏名", # フォームに表示される文字を指定
        validators=[
            DataRequired("氏名は必須です。"), # 入力必須の設定
            Length(1, 30, "30文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
        render_kw={"placeholder": "氏名"}
    )
    teacher_email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"), # 入力必須の設定
            Email("メールアドレスの形式で入力してください。"), # emailの形式で入力するよう設定
        ],
        render_kw={"placeholder": "メールアドレス"}
    )
    teacher_password = PasswordField(
        "パスワード", 
        validators=[
            DataRequired("パスワードは必須です。"), # 入力必須の設定
            Length(8, 25, "8~25文字で入力してください。"),
        ],
        render_kw={"placeholder": "パスワード"}
    )
    teacher_class_num = SelectField(
        "クラス番号",
    )
    teacher_authority = SelectField(
        "管理者権限",
        choices=[(0, "なし"), (1, "あり")],
    )
    submit = SubmitField("登録") # フォームの入力完了ボタンの作成

# LoginFormを作成。フォームを作成する際はとりあえずカッコの中にFlaskFormを書いておく（フォーム作成に必要な機能を使えるようになる）
class TeacherLoginForm(FlaskForm):
    # emailの入力欄を作成
    teacher_id = StringField(
        "教員番号",
        validators=[
            DataRequired("教員番号は必須です。"), # 入力必須の設定
            Length(6, 6, "6文字で入力してください。"),
        ],
        render_kw={"placeholder": "教員番号"}
    )
    teacher_password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードは必須です。")],
        render_kw={"placeholder": "パスワード"}) # パスワードを入力必須に設定
    submit = SubmitField("ログイン")


    # SignUpFormを作成。フォームを作成する際はとりあえずカッコの中にFlaskFormを書いておく（フォーム作成に必要な機能を使えるようになる）
class StudentSignUpForm(FlaskForm):
    student_id = StringField(
        "生徒番号",
        validators=[
            DataRequired("生徒番号は必須です。"), # 入力必須の設定
            Length(7, 7, "7文字で入力してください。"), # 生徒番号は7桁
        ],
        render_kw={"placeholder": "生徒番号"}
    )
    student_name = StringField(  # ユーザネームを入力するフィールドを作成
        "氏名", # フォームに表示される文字を指定
        validators=[
            DataRequired("氏名は必須です。"), # 入力必須の設定
            Length(1, 30, "30文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
        render_kw={"placeholder": "氏名"}
    )
    student_email = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"), # 入力必須の設定
            Email("メールアドレスの形式で入力してください。"), # emailの形式で入力するよう設定
        ],
        render_kw={"placeholder": "メールアドレス"}
    )
    student_password = PasswordField(
        "パスワード", 
        validators=[
            DataRequired("パスワードは必須です。"), # 入力必須の設定
            Length(8, 25, "8~25文字で入力してください。"),
        ],
        render_kw={"placeholder": "パスワード"}
    )
    student_entrollment_year = SelectField(
        "入学年度",
    )
    student_birth_date = DateField(
        "誕生日",
    )
    student_school = SelectField(
        "学校名",
    )
    student_class_num = SelectField(
        "クラス番号",
    )
    submit = SubmitField("登録") # フォームの入力完了ボタンの作成

# LoginFormを作成。フォームを作成する際はとりあえずカッコの中にFlaskFormを書いておく（フォーム作成に必要な機能を使えるようになる）
class StudentLoginForm(FlaskForm):
    student_id = StringField(
        "生徒番号",
        validators=[
            DataRequired("生徒番号は必須です。"), # 入力必須の設定
            Length(7, 7, "7文字で入力してください。"),
        ],
        render_kw={"placeholder": "生徒番号"}
    )
    student_password = PasswordField(
        "パスワード",
        validators=[DataRequired("パスワードは必須です。")],
        render_kw={"placeholder": "パスワード"}
        ) # パスワードを入力必須に設定
    submit = SubmitField("ログイン")

class EmailForm(FlaskForm):
    id = StringField(
        "生徒番号または教員番号",
        validators=[
            DataRequired("生徒番号は必須です。"), # 入力必須の設定
            Length(6, 7, "6~7文字で入力してください。"), # 生徒番号は7桁
        ],
        render_kw={"placeholder": "生徒番号または、教員番号"}
    )
    mail = StringField(
        "メールアドレス",
        validators=[
            DataRequired("メールアドレスは必須です。"), # 入力必須の設定
            Email("メールアドレスの形式で入力してください。"), # emailの形式で入力するよう設定
        ],
        render_kw={"placeholder": "メールアドレス"}
    )
    submit = SubmitField("メールを送信")

class OneTimeForm(FlaskForm):
    onetime = StringField(
        "ワンタイムパスワード",
        validators=[
            DataRequired("ワンタイムパスワードを入力してください"), # 入力必須の設定
            Length(6, 6, "6文字で入力してください。"), # 生徒番号は7桁
        ],
        render_kw={"placeholder": "ワンタイムパスワード"}
    )
    submit = SubmitField("確定")

class NewPwForm(FlaskForm):
    password1 = PasswordField(
        "新しいパスワード",
        validators=[
            DataRequired("パスワードは必須です。"), # 入力必須の設定
            Length(8, 25, "8~25文字で入力してください。"),
        ],
        render_kw={"placeholder": "新しいパスワード"}
    )
    password2 = PasswordField(
        "再確認",
        validators=[
            DataRequired("パスワードは必須です。"), # 入力必須の設定
            Length(8, 25, "8~25文字で入力してください。"),
        ],
        render_kw={"placeholder": "再確認"}
    )
    submit = SubmitField("確定")