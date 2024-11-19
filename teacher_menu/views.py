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
def t_menu():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    # ログインしている教員の情報を取得
    teacher = current_user
            
    # ユーザーがアイコンを設定していない場合はデフォルトのパスを使用
    if not teacher.icon_path or not os.path.exists(os.path.join(current_app.root_path, teacher.icon_path)):
        teacher.icon_path = 'uploads/icon/default/default_icon.png'
        
    return render_template("teacher_menu/index.html", teacher=teacher)