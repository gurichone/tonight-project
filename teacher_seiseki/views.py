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
@seiseki.route("/", methods=["GET", "POST"])
def teacher_seiseki():
    form = SearchScore()
    if form.validate_on_submit():
        # 科目名、クラス番号、生徒番号から絞り込みをする
        score = Score()

        db.session.query(Score).fliter(Score.subject_name=="",
                                       Score.class_num=="",
                                       Score.student_num=="").all()
        
    return render_template("tempaltes/teacher_seiseki/seiseki.html", form=form)