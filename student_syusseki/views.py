from flask import Blueprint, render_template, redirect, url_for, request, session
from app import db
from flask_login import current_user, login_required
from teacher_seiseki.models import Score
from auth.models import Student, Subject
from student_syusseki.forms import AttendCheck

syusseki = Blueprint(
    "syusseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@syusseki.route("/", methods=["GET", "POST"])
@login_required
def s_syusseki():
    if len(current_user.id) != 7:
        return render_template("student/gohb.html")

    attend = AttendCheck()

    if attend.validate_on_submit():
        # 出席を記録する処理
        student = db.session.query(Student).filter(Student.id == current_user.id).first()  # 生徒IDを取得
        score = (
            db.session.query(Score)
            .filter_by(id=student.id)
            .join(Subject, Subject.subject_id == Score.subject_id)
            .first()
        )

        if score:
            score.attend_day += 1
            db.session.commit()
            return render_template(
                "student_syusseki/attend_complete.html",
                attend=attend,
                student_id=student.id,
                score=score,
            )
        else:
            # 同じページに遷移する
            return render_template("student_syusseki/attend.html", form=attend)

    return render_template("student_syusseki/attend.html", form=attend)
