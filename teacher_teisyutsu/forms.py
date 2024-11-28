from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DateField, StringField
from wtforms.validators import DataRequired, Length, ReadOnly
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
        choices=[(0, "指定なし"), (1, "効果測定"), (2, "演習問題")],
        coerce=int,
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成

class CreateSubmissionForms(FlaskForm):
    name = StringField(
        "提出物名", # フォームに表示される文字を指定
        validators=[
            DataRequired(message="入力は必須です。"),  # 入力必須の設定
            Length(0, 30, "30文字以内で入力してください。"), # 教員番号は6桁
            
        ],
        render_kw={"placeholder": "提出物名"}
    )
    subject = SelectField(
        "科目名", # フォームに表示される文字を指定
        validators=[
             DataRequired(message="入力は必須です。"), 
        ],
        coerce=int,
        render_kw={"placeholder": "科目名"}
    )
    type = SelectField(
        "実施内容", # フォームに表示される文字を指定
        choices=[(1, "効果測定"), (2, "演習問題")],
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
        ],
        render_kw={"placeholder": "問題文"}
    )
    testcase = TextAreaField(
        "テストケース",
        validators=[
        ],
    )
    submit = SubmitField("確定") # フォームの送信ボタンを作成




