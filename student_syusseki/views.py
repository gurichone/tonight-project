from flask import Blueprint, render_template, session, flash
from flask_login import current_user, login_required
from teacher_seiseki.models import Score, Syusseki
from auth.models import Student 
from student_syusseki.forms import AttendCheck
from teacher_jikanwari.models import Timetable
from datetime import datetime, timedelta
from app import db
import hashlib

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
    # code_time = None  
    # if 'code_timestamp' in session:
    #     code_time = datetime.fromtimestamp(session['code_timestamp'])
    # else:
    #     return render_template("student_syusseki/code_not_in_session.html", form=AttendCheck())

    # コードの有効期限チェック
    # if datetime.now() - code_time > timedelta(minutes=5):
    #     session.pop('attendance_code', None)
    #     session.pop('code_timestamp', None)
    #     flash("コードの有効期限が切れました。再発行してください。", "error")  # 有効期限切れのメッセージを表示
    #     return render_template("student_syusseki/attend.html", form=AttendCheck())

    attend = AttendCheck()

    if attend.validate_on_submit():
        period=0
        now = datetime.now()
        for p in range(1, 4):
            code_data = f"{now.strftime('%Y%m%d')}{p}" + "jn;zsbvuo;bbh;rlznnzibvnbrnl.fbk;lnk.szv;bab"
            code_hash = hashlib.sha256(code_data.encode()).hexdigest()[:6]
            print(code_hash, attend.attendance_code.data)
            if attend.attendance_code.data == code_hash:
                period = p
                break
        # timetable = (
        #     db.session.query(Timetable)
        #     .filter_by(year=now.year, month=now.month, day=now.day)
        #     .first()
        # )
        # 出席を記録する処理
        # student = db.session.query(Student).filter(Student.id == current_user.id).first()
        # score = db.session.query(Score).filter_by(id=student.id).first()


        # score.attend_day += 1
        # db.session.commit()
        if period == 0:
            flash("出席コードが違います")
            return render_template("student_syusseki/attend.html", form=attend)
            
        else:
            syusseki = db.session.query(Syusseki).filter_by(student_id=current_user.id, year=now.year, month=now.month, day=now.day, periods=period).first()
            if syusseki:
                flash("出席済みです")
                return render_template("student_syusseki/attend.html", form=attend)
            syusseki = Syusseki(
                student_id = current_user.id,
                year = now.year,
                month = now.month,
                day = now.day,
                periods = period
            )
            db.session.add(syusseki)
            db.session.commit()
            subjects = db.session.query(Timetable).filter_by(year=now.year, month=now.month, day=now.day, class_num=current_user.class_num).first()

            if period == 1:
                subject=subjects.period1
                score = db.session.query(Score).filter_by(id=current_user.id, subject_id=subjects.period1).first()
            if period == 2:
                subject=subjects.period2
                score = db.session.query(Score).filter_by(id=current_user.id, subject_id=subjects.period2).first()
            if period == 3:
                subject=subjects.period3
                score = db.session.query(Score).filter_by(id=current_user.id, subject_id=subjects.period3).first()
            if score:
                if score is None:
                    score = Score(
                        id=current_user.id,
                        class_num=current_user.class_num,
                        subject_id=subject,
                        attend_day=1
                    )
                    db.session.add(score)
                    db.session.commit()
                elif score.attend_day is None:
                    score.attend_day = 1
                    db.session.add(score)
                    db.session.commit()
                else:
                    score.attend_day += 1
                    db.session.add(score)
                    db.session.commit()
            else:
                score = Score(
                    id=current_user.id,
                    class_num=current_user.class_num,
                    subject_id=subject,
                    attend_day = 1
                )
                db.session.add(score)
                db.session.commit()

            return render_template(
                "student_syusseki/attend_complete.html",
            )

    return render_template("student_syusseki/attend.html", form=attend)
