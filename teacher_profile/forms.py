from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class ProfileImageForm(FlaskForm):
    profile_image = FileField('画像を選択', validators=[
        DataRequired(), 
        FileAllowed(['jpg', 'jpeg', 'png'], '画像ファイルのみアップロードできます。')
    ])
    submit = SubmitField('アップロード')
