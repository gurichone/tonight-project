from flask import Blueprint, render_template, redirect, url_for, session, current_app, send_file
from flask_login import current_user, login_required
from app import db
from teacher_teisyutsu.models import Submission, Personal_Submission
from auth.models import Subject, Student
import shutil
from pathlib import Path

saiten = Blueprint(
    "saiten",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@saiten.route("/<submission_id>/")
@login_required
def t_saiten(submission_id):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission = db.session.query(Submission, Subject).join(Submission, Submission.subject_id==Subject.subject_id).filter_by(submission_id=submission_id).first()
    personal = db.session.query(Personal_Submission, Student).join(Personal_Submission, Personal_Submission.student_id==Student.id).filter_by(submission_id=submission_id).all()
    session["submission"] = submission_id
    return render_template("teacher_saiten/index.html", submission=submission, personal=personal)

@saiten.route("/manual")
@login_required
def manual():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission = db.session.query(Submission, Subject).join(Submission, Submission.subject_id==Subject.subject_id).filter_by(submission_id=session["submission"]).first()
    filename=submission.Submission.submission_name
    shutil.make_archive(filename, format="zip", root_dir=Path(current_app.config["SUBMIT_FOLDER"]), base_dir=Path(str(submission.Submission.submission_id)))
    return send_file(filename + ".zip")


@saiten.route("/auto")
@login_required
def auto():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")