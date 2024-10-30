from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from teacher_teisyutu.forms import SubmissionForms, CreateSubmissionForms
from teacher_teisyutu.models import Subject, Course, Submission, SubmissionSituation
from auth.models import Teacher


teisyutu = Blueprint(
    "teisyutu",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@teisyutu.route("/")
def t_teisyutu():
    course = db.session.query(Course).filter_by(class_num = current_user.class_num).first()
    submissions = db.session.query(Submission).filter_by(course_name = course).all()