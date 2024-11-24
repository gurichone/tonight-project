from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import current_user, login_required
from app import db
from teacher_sent.models import Get_Information
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
    if len(current_user.id) != 7:
        return render_template("student/gohb.html")
    # ログインしている生徒の情報を取得
    student = current_user
    # 未読の通知があるか確認
    new = db.session.query(Get_Information).filter_by(student_num=student.id, read=0).all()
    # ユーザーがアイコンを設定していない場合はデフォルトのパスを使用
    if not student.icon_path or not os.path.exists(os.path.join(current_app.root_path, student.icon_path)):
        student.icon_path = 'uploads/icon/default/default_icon.png'

    return render_template('student_menu/menu.html', student=student, new=len(new))