from flask import Blueprint, render_template, session, flash
from flask_login import current_user, login_required
from teacher_seiseki.models import Score
from auth.models import Student 
from student_syusseki.forms import AttendCheck
from datetime import datetime, timedelta
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
    
    # `code_time` の初期化
    code_time = None  
    if 'code_timestamp' in session:
        code_time = datetime.fromtimestamp(session['code_timestamp'])
    else:
        return render_template("student_syusseki/code_not_in_session.html", form=AttendCheck())

    # コードの有効期限チェック
    if datetime.now() - code_time > timedelta(minutes=5):
        session.pop('attendance_code', None)
        session.pop('code_timestamp', None)
        flash("コードの有効期限が切れました。再発行してください。", "error")  # 有効期限切れのメッセージを表示
        return render_template("student_syusseki/attend.html", form=AttendCheck())

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
