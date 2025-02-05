from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, length, NumberRange

# 成績を検索する際の絞り込みに必要なフォームクラスを作成
class SearchScore(FlaskForm):
    subject_id = SelectField("科目名")

    class_num = SelectField("クラス番号")

    student_name = StringField("氏名")

    submit = SubmitField("")

# データベースに成績を追加するためのフォームクラスを作成 
class AddScore(FlaskForm):   
    # ここの入力でscoreテーブルのstudent_numとStudentテーブルのidを関連付け、氏名を判別
    id = SelectField(
        "生徒番号",
        validators=[
            DataRequired(message="生徒番号の選択は必須です。"),
        ]
    )

    student_name = StringField(
        "氏名",
        )

    subject_id = SelectField(
        "科目名",
        validators=[
            DataRequired(message="科目名の選択は必須です。"),
        ]
    )

    assessment_id = SelectField(
        "評価",
        choices=[
            ('A','A'),('B','B'),('C','C'),('D','D'),('E','E')
        ]
    )

    submit = SubmitField("登録")

# 出席日数を絞り込みするフォームを作成
class AttendScore(FlaskForm):

    student_name = SelectField("氏名")

    year = SelectField("年",coerce=int,)

    month = SelectField("月",coerce=int,)

    submit = SubmitField("")

# 成績の編集を行うためのフォームを作成
class EditScore(FlaskForm):
    assessment_id = SelectField(
        "評価",
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E")],
    )

    attend_day = IntegerField(
        "出席回数",
        validators=[
            # DataRequired("この欄は必ず入力してください。"),
            NumberRange(min=0, max=2100000000)
        ]
    )
