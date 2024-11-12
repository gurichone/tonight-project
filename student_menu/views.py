from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import current_user, login_required
from app import db
import os



menu = Blueprint(
    "menu",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@menu.route("/")
@login_required
def s_menu():
    # ログインしている生徒の情報を取得
    student = current_user

    # ユーザーがアイコンを設定していない場合はデフォルトのパスを使用
    if not student.icon_path or not os.path.exists(os.path.join(current_app.root_path, student.icon_path)):
        student.icon_path = 'uploads/icon/default/default_icon.png'

    return render_template('student_menu/menu.html', student=student)