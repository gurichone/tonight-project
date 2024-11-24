from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from teacher_sent.models import Information, Get_Information
from auth.models import Teacher


notice = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@notice.route("/")
@login_required
def s_notice():
    if len(current_user.id) != 7:
        return render_template("student/gohb.html")
    notice=db.session.query(Information, Get_Information, Teacher).join(Information, Teacher.id==Information.teacher_num).order_by("sent_time").join(Get_Information, Get_Information.info_id==Information.info_id).filter_by(student_num=current_user.id).all()
    # 未読のデータを取り出し既読にする
    new = db.session.query(Get_Information).filter_by(student_num=current_user.id, read=0).all()
    for n in new:
        n.read=1
        db.session.add(n)
        db.session.commit()
    return render_template("student_notice/notice.html", notice=notice)