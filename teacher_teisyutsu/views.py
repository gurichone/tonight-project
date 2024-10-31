from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from teacher_teisyutsu.forms import SubmissionForms, CreateSubmissionForms
from teacher_teisyutsu.models import Subject, Course, Submission, SubmissionSituation
from auth.models import Teacher


teisyutu = Blueprint(
    "teisyutu",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@teisyutu.route("/", methods=["GET", "POST"])
def t_teisyutsu():
    form = SubmissionForms()
    subjects = db.session.query(Subject).all()
    form.subject.choices=[(s.subject_id, s.subject_name)for s in subjects]
    if form.validate_on_submit():
        # filter_byにformの入力内容を追加
        submissions = db.session.query(Submission).join(Submission,Submission.subject_id==Subject.subject_id).filter_by(class_num = current_user.class_num, subject_id=form.subject.data, submission_type=form.type.data).all()
        return render_template("teacher_teisyutsu/admin.html", submissions=submissions, form=form, subject=db.session)
    # ログインしているユーザーのクラスで絞る
    submissions = db.session.query(Submission, Subject).join(Submission,Submission.subject_id==Subject.subject_id).filter_by(class_num = current_user.class_num).all()
    return render_template("teacher_teisyutsu/admin.html", submissions=submissions, form=form)