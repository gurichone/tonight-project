from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
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
def s_notice():
    notice=db.session.query(Information, Get_Information, Teacher).join(Information, Teacher.id==Information.teacher_num).order_by("sent_time").join(Get_Information, Get_Information.info_id==Information.info_id).filter_by(student_num=current_user.id).all()
    return render_template("student_notice/notice.html", notice=notice)