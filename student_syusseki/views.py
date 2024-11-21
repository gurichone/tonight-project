from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import db
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from teacher_seiseki.models import Score
from auth.models import Student
from student_syusseki.forms import AttendCheck

syusseki = Blueprint(
    "syusseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

def is_code_valid():
    code_timestamp = session.get('code_timestamp')
    if code_timestamp:
        # コードが発行されてから1分が経過したかを確認
        issue_time = datetime.fromtimestamp(code_timestamp)
        if datetime.now() <= issue_time + timedelta(minutes=1):
            return True  # コードは有効
    return False  # コードは無効

@syusseki.route("/", methods=["GET", "POST"])
@login_required
def s_syusseki():
    if len(current_user.id) != 7:
        return render_template("student/gohb.html")
    
    # フォームのインスタンスの作成
    attend = AttendCheck()
    
    # ここでページに入力されたコードを取得
    attend_code = request.form.get("attendance_code")
    # 一時保存されたコードと時刻を取得
    saved_code = session.get("attendance_code")
    code_timestamp = session.get("code_timestamp")

    if attend.validate_on_submit():
        # 1分の有効期限チェック
        if saved_code and code_timestamp:
            if is_code_valid():  # 1分以内なら有効
                if attend_code == saved_code:
                    # 出席を記録する処理
                    student_id = db.session.query(Student).filter(current_user.id == Student.id).first()  # 生徒IDを取得
                    score = db.session.query(Score).filter_by(id=student_id).first()
                    
                    if score:
                        score.attend_day += 1
                        db.session.commit()
                        return render_template(
                            "student_syusseki/attend_complete.html",
                            attend=attend,
                            student_id=student_id,
                            score=score
                            )
                    # 諸エラー
                    else:
                        flash("生徒IDが見つかりません。", "error")
                else:
                    flash("コードが一致しません。", "error")
            else:
                flash("出席コードの有効期限が切れています。", "error")
        else:
            flash("有効なコードが発行されていません。", "error")
        
    return render_template("student_syusseki/attend.html")