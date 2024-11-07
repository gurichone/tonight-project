#gvuihbjhgvhuygibjhvyuihjkbh
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DateField, StringField
from wtforms.validators import DataRequired, length, ReadOnly
from flask_wtf.file import FileAllowed, FileField, FileRequired


class SubmissionForms(FlaskForm): #ユーザー新規作成とユーザー編集用のクラスを作成(forms.pyではとりあえずFlaskFormを継承しておく)
    # イベントを入力するフィールドを作成
    subject = SelectField(
        "科目名", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
        ],
    )
    type = SelectField(
        "実施内容", # フォームに表示される文字を指定
        choices=[(1, "効果測定"), (2, "演習問題")],
        coerce=int
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成

class CreateSubmissionForms(FlaskForm):
    name = StringField(
        "提出物名", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
        ],
    )
    subject = SelectField(
        "科目名", # フォームに表示される文字を指定
        validators=[
             DataRequired(message="入力は必須です。"), 
        ],
        coerce=int
    )
    type = SelectField(
        "実施内容", # フォームに表示される文字を指定
        choices=[(0, "指定なし"), (1, "効果測定"), (2, "演習問題")],
        validators=[],
        coerce=int
    )
    rimit = DateField(
        "提出期限",
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
        ],
    )
    scoring_type = SelectField(
        "採点方法",
        choices=[(0, "採点方法なし"), (1, "テストケースによる採点"), (2, "生成AIによる採点"), (3, "テストケースによる採点とAIによる採点")],
        validators=[],
        coerce=int
        
    )
    question = TextAreaField(
        "問題文", # フォームに表示される文字を指定
        validators=[
             DataRequired(message="入力は必須です。"), 
        ],
    )
    testcase = TextAreaField(
        "テストケース",
        validators=[
             DataRequired(message="入力は必須です。"), 
        ],
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成




