from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import current_user, login_required
from app import db
from teacher_teisyutsu.models import Personal_Submission, Submission
from student_teisyutsu.forms import SubmitForms
from pathlib import Path


teisyutsu = Blueprint(
    "teisyutsu",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@teisyutsu.route("/")
@login_required
def s_teisyutsu_index():
    if len(current_user.id) != 7:
        return render_template("student/gohb.html")
    submission=db.session.query(Personal_Submission, Submission).join(Personal_Submission, Personal_Submission.submission_id==Submission.submission_id).filter_by(student_id=current_user.id).all()
    return render_template("student_teisyutsu/index.html", submission=submission)

@teisyutsu.route("/teisyutsu/<submission_id>", methods=["GET", "POST"])
@login_required
def s_teisyutsu(submission_id):
    if len(current_user.id) != 7:
        return render_template("student/gohb.html")
    form=SubmitForms()
    if form.validate_on_submit():
        file = form.file.data
        #拡張子を抽出
        ext = Path(file.filename).suffix
        code_uuid_file_name = submission_id + "/" + current_user.id + '_' + current_user.student_name + ext

        code_path =Path(
            current_app.config["SUBMIT_FOLDER"], code_uuid_file_name
            )
        file.save(code_path)


        ps = db.session.query(Personal_Submission).filter_by(submission_id=submission_id, student_id=current_user.id).first()
        ps.file=code_uuid_file_name
        db.session.add(ps)
        db.session.commit()
        ps.submitted=1
        db.session.add(ps)
        db.session.commit()

        return render_template("student_teisyutsu/submit_done.html")
    submission=db.session.query(Submission).filter_by(submission_id=submission_id).first()
    return render_template("student_teisyutsu/submit.html", form=form, submission=submission)