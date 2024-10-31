from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, DateTimeField, StringField, ValidationError
from wtforms.validators import DataRequired, Length

class StudentSearch(FlaskForm):
        id = SelectField("生徒番号")

        class_num = SelectField("クラス番号")

        student_name = StringField("氏名")

        submit = SubmitField("検索")

        def validate_student_num(self, id):
            # バリデーション内容：生徒番号は7桁以外は禁止
            len_id = str(id)
            if len_id != len(7):
                raise ValidationError("生徒番号は7桁で入力してください")
            
            