from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired

# 成績を検索する際の絞り込みに必要なフォームクラスを作成
class SearchScore(FlaskForm):
    subject_name = SelectField("科目名")

    class_num = SelectField("クラス番号")

    student_name = StringField("氏名")

    submit = SubmitField("検索")

    # バリデーションは未実装
    # def validate_student_num(self, student_num):
    #     # バリデーション内容：生徒番号は7桁以外は禁止
    #     len_stu_num = str(student_num)
    #     if len_stu_num != len(7):
    #         raise ValidationError("生徒番号は7桁で入力してください")

#データベースに成績を追加するためのフォームクラスを作成 
class AddScore(FlaskForm):
    student_num = StringField("生徒番号")

    student_name = StringField("氏名")

    subject_name = StringField("科目名")

    assessment_id = StringField("評価")

    submit = SubmitField("登録")