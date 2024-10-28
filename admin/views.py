from flask import Blueprint, flash, redirect, render_template, request, url_for
from app import db 
from admin.forms import CourseForm, SubjectForm
from auth.models import Teacher, Student 
from teacher_teisyutu.models import Subject, Course, Submission, SubmissionSituation


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/")
def admin_is_god():
    course_form = CourseForm()
    if course_form.validate_on_submit():
        return "courseテーブルに保存しました"
    return render_template("admin/admin.html", course_form=course_form)