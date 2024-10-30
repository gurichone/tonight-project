#gvuihbjhgvhuygibjhvyuihjkbh
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DateTimeField, StringField
from wtforms.validators import DataRequired, length
from flask_wtf.file import FileAllowed, FileField, FileRequired


class SubmissionForms(FlaskForm): #ユーザー新規作成とユーザー編集用のクラスを作成(forms.pyではとりあえずFlaskFormを継承しておく)
    # イベントを入力するフィールドを作成
    subject = SelectField(
        "科目名", # フォームに表示される文字を指定
        coerce=int
    )
    type = SelectField(
        "実施内容", # フォームに表示される文字を指定
        choices=[(1, "効果測定"), (2, "演習問題")],
        coerce=int
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成

class CreateSubmissionForms(FlaskForm):
    subject = SelectField(
        "科目名", # フォームに表示される文字を指定
        coerce=int
    )
    name = StringField(
        "提出物名", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
            # length(max=20, message="20文字以内で入力してください。"), # 文字数を1~30文字に設定
        ],
    )
    type = SelectField(
        "実施内容", # フォームに表示される文字を指定
        coerce=int
    )
    rimit = DateTimeField(
        "提出期限",
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
        ],
    )
    Scoring_type = SelectField(
        "採点方法",
        choices=[(1, "テストケースによる採点"), (2, "生成AIによる採点"), (3, "テストケースによる採点とAIによる採点"), (4, "採点方法なし")]
        
    )
    question = TextAreaField(
        "問題文", # フォームに表示される文字を指定
    )
    testcase = TextAreaField(
        "テストケース"
    )