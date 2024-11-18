from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class PointForm(FlaskForm):
    fieldlist = dict()
    def __init__(self, studentlst):
        for s in studentlst:
            self.fieldlist[s["id"]] = IntegerField(
                s["name"], # フォームに表示される文字を指定
                validators=[
                    DataRequired("入力は必須です。"),
                    NumberRange(min=0, max=100, message="0~100で入力してください"),  # 入力必須の設定
                ],
            )
    submit = SubmitField("確定")