from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app import db
from flask_login import current_user, login_required
from datetime import datetime, timedelta
from teacher_seiseki.models import Score
from auth.models import Student
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
    if request.method == "POST":
        input_code = request.form.get("attendance_code")
        
        # 一時保存されたコードと時刻を取得
        saved_code = session.get("attendance_code")
        code_timestamp = session.get("code_timestamp")

        # 1分の有効期限チェック
        if saved_code and code_timestamp:
            time_diff = datetime.now().timestamp() - code_timestamp
            if time_diff <= 60:  # 1分以内なら有効
                if input_code == saved_code:
                    # 出席を記録する処理
                    student_id = request.form.get("student_id")  # 生徒IDを入力させるか別途取得
                    score = db.session.query(Score).filter_by(id=student_id).first()
                    
                    if score:
                        score.attend_day += 1
                        db.session.commit()
                        flash("出席が登録されました。", "success")
                    else:
                        flash("生徒IDが見つかりません。", "error")
                else:
                    flash("コードが一致しません。", "error")
            else:
                flash("出席コードの有効期限が切れています。", "error")
        else:
            flash("有効なコードが発行されていません。", "error")
        
    return render_template("student_syusseki/attend.html")