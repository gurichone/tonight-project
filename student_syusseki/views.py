from flask import Blueprint, render_template, session
from flask_login import current_user, login_required
from teacher_seiseki.models import Score
from auth.models import Student 
from student_syusseki.forms import AttendCheck
from datetime import datetime,timedelta
from app import db

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
    
    if 'code_timestamp' in session:
        code_time = datetime.fromtimestamp(session['code_timestamp'])
    if datetime.now() - code_time > timedelta(minutes=5):
        session.pop('attendance_code', None)
        session.pop('code_timestamp', None)

    attend = AttendCheck()

    if attend.validate_on_submit():
        # 出席を記録する処理
        student = db.session.query(Student).filter(Student.id == current_user.id).first()
        score = db.session.query(Score).filter_by(id=student.id).first()

        if score:
            score.attend_day += 1
            db.session.commit()
            return render_template(
                "student_syusseki/attend_complete.html",
                attend=attend,
                student_id=student.id,
                score=score,
            )

    return render_template("student_syusseki/attend.html", form=attend)
