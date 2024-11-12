from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, length

# 成績を検索する際の絞り込みに必要なフォームクラスを作成
class SearchScore(FlaskForm):
    subject_id = SelectField("科目名")

    class_num = SelectField("クラス番号")

    student_name = StringField("氏名")

    submit = SubmitField("検索")

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
            ("","--"),('A','A'),('B','B'),('C','C'),('D','D'),('E','E')
        ],
        validators=[
            DataRequired(message="成績を付けてください。")
        ]
    )

    submit = SubmitField("登録")

# 出席日数を絞り込みするフォームを作成
class AttendScore(FlaskForm):
    subject_id = SelectField("科目名")

    class_num = SelectField("クラス番号")

    student_name = StringField("氏名")

    submit = SubmitField("検索")