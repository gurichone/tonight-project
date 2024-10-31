from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from teacher_teisyutsu.forms import SubmissionForms, CreateSubmissionForms
from teacher_teisyutsu.models import Submission, Personal_Submission
from auth.models import Subject, Course
from auth.models import Teacher


teisyutsu = Blueprint(
    "teisyutsu",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@teisyutsu.route("/", methods=["GET", "POST"])
def t_teisyutsu():
    form = SubmissionForms()
    subjects = db.session.query(Subject).all()
    form.subject.choices=[(s.subject_id, s.subject_name)for s in subjects]
    if form.validate_on_submit():
        # filter_byにformの入力内容を追加
        submissions = db.session.query(Submission, Subject).join(Submission,Submission.subject_id==Subject.subject_id).filter_by(class_num = current_user.class_num, subject_id=form.subject.data, submission_type=form.type.data).all()
        return render_template("teacher_teisyutsu/admin.html", submissions=submissions, form=form, subject=db.session.query(Subject).filter_by(subject_id = form.subject.data).first())
    # ログインしているユーザーのクラスで絞る
    submissions = db.session.query(Submission, Subject).join(Submission,Submission.subject_id==Subject.subject_id).filter_by(class_num = current_user.class_num).all()
    return render_template("teacher_teisyutsu/admin.html", submissions=submissions, form=form)

# @teisyutsu.route("/add", methods=["GET, POST"])
# def t_teisyutsu_add():
#     form = CreateSubmissionForms()
#     subjects = db.session.query(Subject).all()
#     form.subject.choices=[(s.subject_id, s.subject_name)for s in subjects]
#     if form.validate_on_submit():
