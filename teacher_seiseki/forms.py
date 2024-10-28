from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired

# 成績の科目を選択するフォームクラスを作成
class SearchScore(FlaskForm):
    subject_name = SelectField("科目名")

    class_num = SelectField("クラス番号")

    student_num = IntegerField("生徒番号")

    submit = SubmitField("検索")
