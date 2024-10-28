from flask import Blueprint, render_template, redirect, url_for, request
from app import db
from teacher_seiseki.forms import SearchScore
from teacher_seiseki.models import Score

seiseki = Blueprint(
    "seiseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 成績画面は三つの要素から絞り込みをして検索する
@seiseki.route("/")
def search():
    form = SearchScore()
    # 欄に一つでも入力があれば応答する
    if form.validate_on_submit():
        # 科目名、クラス番号、生徒番号から絞り込みをする
        score = Score(
            subject_name = form.subject_name.data,
            class_num = form.class_num.data,
            student_num = form.student_num.data,
        )
        db.session.query(Score).fliter_by(score)
        
    return render_template("/teacher_seiseki/index.html")

@seiseki.route("/add", methods=["GET"])
def add():
    return None

@seiseki.route("/attendance")
def attendance():
    return None