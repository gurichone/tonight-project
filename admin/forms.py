from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class CourseForm(FlaskForm):
    course_name = StringField(
        "コース名",
        validators=[
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )
    submit = SubmitField("登録")

class SubjectForm(FlaskForm):
    subject_name = StringField(
        "科目名",
        validators=[
            Length(1, 20, "20文字以内で入力してください。"),
        ],
    )
    submit = SubmitField("登録")

class SchoolForm(FlaskForm):
    school_name = StringField(
        "学校名",
        validators=[
            Length(1, 30, "30文字以内で入力してください。"),
        ],
    )
    submit = SubmitField("登録")

class ClassNumForm(FlaskForm):
    class_num = StringField(
        "クラス番号",
        validators=[
            Length(4, 4, "4文字で入力してください。"),
        ],
    )
    course = SelectField(
        "コース名",
    )
    submit = SubmitField("登録")

class CourseSubjectForm(FlaskForm):
    course = SelectField(
        "コース名",
    )
    subject = SelectField(
        "科目名"
    )
    submit = SubmitField("登録")

class StudentAddForm(FlaskForm):
    student_id = StringField(
        "生徒番号",
        validators=[
            DataRequired("生徒番号は必須です。"), # 入力必須の設定
            Length(7, 7, "7文字で入力してください。"),
        ],
    )
    name = StringField(  # ユーザネームを入力するフィールドを作成
        "氏名", # フォームに表示される文字を指定
        validators=[
            DataRequired("氏名は必須です。"), # 入力必須の設定
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
    entrollment_year = SelectField(
        "入学年度",
    )
    birth_date = DateField(
        "誕生日",
    )
    school = SelectField(
        "学校名",
    )
    class_num = SelectField(
        "クラス番号",
    )
    submit = SubmitField("登録")