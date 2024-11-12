from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from flask_login import current_user, login_required
from auth.models import School, Course
from app import db
from teacher_profile.forms import ProfileImageForm
import os
from werkzeug.utils import secure_filename
import time

prof = Blueprint(
    "profile",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@prof.route('/')
@login_required
def profile():
    # ログインしている生徒の情報を取得
    student = current_user

     # 学校名とコース名を取得
    school = School.query.filter_by(school_id=student.school_id).first()
    course = Course.query.filter_by(course_id=student.course_id).first()

    # ユーザーがアイコンを設定していない場合はデフォルトのパスを使用
    if not student.icon_path or not os.path.exists(os.path.join(current_app.root_path, student.icon_path)):
        student.icon_path = 'uploads/icon/default/default_icon.png'
        
    return render_template(
        'student_profile/profile.html',
        student=student,
        school_name=school.school_name if school else "不明",
        course_name=course.course_name if course else "不明"
        )

@prof.route('/edit_profile_image', methods=['GET', 'POST'])
@login_required
def edit_profile_image():
    form = ProfileImageForm()
    if form.validate_on_submit():
        # アップロードディレクトリのパスを取得 (static外のuploads/iconフォルダ)
        upload_folder = os.path.join(current_app.root_path, 'uploads', 'icon', str(current_user.id))
        
        # 生徒IDごとのフォルダが存在しない場合は作成
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 新しい画像のファイル名を生成 (タイムスタンプを追加)
        file = form.profile_image.data
        filename = secure_filename(file.filename)
        file_extension = os.path.splitext(filename)[1]  # 拡張子を取得
        new_filename = f"{int(time.time())}{file_extension}"  # タイムスタンプをファイル名に
        
        # 新しい画像の保存パス
        file_path = os.path.join(upload_folder, new_filename)
        
        # 既存の画像があれば削除
        if current_user.icon_path and current_user.icon_path != 'images/default_icon.png':
            old_file_path = os.path.join(current_app.root_path, 'uploads', current_user.icon_path)
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
        
        # 新しい画像を保存
        file.save(file_path)
        
        # ユーザーのicon_pathを更新 (教員IDに基づくパス)
        current_user.icon_path = f'uploads/icon/{current_user.id}/{new_filename}'
        db.session.commit()
        
        flash('プロフィール画像が更新されました。', 'success')
        return redirect(url_for('teacher.profile.profile'))

    return render_template('teacher_profile/edit_profile_image.html', form=form)

@prof.route('/uploads/icon/<path:filename>')
def upload_file(filename):
    # uploads/iconディレクトリのパス
    upload_folder = os.path.join(current_app.root_path, 'uploads', 'icon')
    
    # デバッグ: パスが正しいか確認
    # print(f"Uploading file from: {upload_folder}/{filename}")

    return send_from_directory(upload_folder, filename)

@prof.route('/reset_profile_image', methods=['POST'])
@login_required
def reset_profile_image():
    # 現在のアイコンがあれば削除
    if current_user.icon_path and current_user.icon_path != 'uploads/icon/default/default_icon.png':
        old_file_path = os.path.join(current_app.root_path, 'uploads', current_user.icon_path)
        if os.path.exists(old_file_path):
            os.remove(old_file_path)
    
    # デフォルトアイコンに設定
    current_user.icon_path = 'uploads/icon/default/default_icon.png'
    db.session.commit()
    
    flash('プロフィール画像がデフォルトに戻されました。', 'success')
    return redirect(url_for('teacher.profile.profile'))

