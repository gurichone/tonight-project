from flask import Blueprint, render_template, redirect, url_for

from app import db
from .models import Timetable  # 時間割データを取得するためにモデルをインポート

jikanwari = Blueprint(
    "jikanwari",  # Blueprint名
    __name__,
    template_folder="templates",
    static_folder="static"
)

@jikanwari.route("/")
def s_jikanwari():
    # 時間割表のデータを取得
    data = Timetable.query.all()  # 必要に応じてフィルタリング
    return render_template("student_jikanwari/table.html", data=data)