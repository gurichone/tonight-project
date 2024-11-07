from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db

menu = Blueprint(
    "menu",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@menu.route("/")
@login_required
def t_menu():
    # ログインしている教員の情報を取得
    teacher = current_user
    return render_template("teacher_menu/index.html", teacher=teacher)