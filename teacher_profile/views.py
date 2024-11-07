from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import current_user, login_required
from auth.models import Teacher
from app import db
from .forms import ProfileImageForm
import os
from werkzeug.utils import secure_filename


prof = Blueprint(
    "profile",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@prof.route('/')
@login_required
def profile():
    # ログインしている教員の情報を取得
    teacher = current_user

    return render_template('teacher_profile/profile.html', teacher=teacher)


@prof.route('/edit_profile_image', methods=['GET', 'POST'])
@login_required
def edit_profile_image():
    form = ProfileImageForm()
    if form.validate_on_submit():
        # アップロードディレクトリのパスを取得
        upload_folder = os.path.join(current_app.static_folder, 'uploads')
        
        # アップロードディレクトリが存在しない場合は作成
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # ファイルの保存処理
        file = form.profile_image.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # ユーザーのicon_pathを更新
        current_user.icon_path = f'uploads/{filename}'
        db.session.commit()
        flash('プロフィール画像が更新されました。', 'success')
        
        return redirect(url_for('teacher.profile.profile'))

    return render_template('teacher_profile/edit_profile_image.html', form=form)