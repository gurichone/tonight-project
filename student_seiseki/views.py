from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app import db
from auth.models import Subject
from teacher_seiseki.models import Score

seiseki = Blueprint(
    "seiseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@seiseki.route("/", methods=["GET","POST"])
@login_required
def s_seiseki():
    if len(current_user.id) != 7:
        return render_template("student/gohb.html")
    
    scores = db.session.query(Score, Subject.subject_name).join(
        Subject, Score.subject_id == Subject.subject_id
    ).filter(Score.id == current_user.id).all()

    if not scores:
        flash("あなたのデータは登録されていないか、取得に失敗しました。")
        return render_template("student_seiseki/student_scores.html", scores=None)
    
    return render_template("student_seiseki/student_scores.html", scores=scores)