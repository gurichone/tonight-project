from flask import Blueprint, flash, redirect, render_template, request, url_for
from app import db 
from admin.forms import CourseForm, SubjectForm
from auth.models import Teacher, Student 
from teacher_teisyutu.models import Subject, Course, Submission, SubmissionSituation


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/")
def admin_menu():
    return render_template("admin/admin.html", message="お前が管理者だ")

@admin.route("/course", methods=["GET", "POST"])
def course():
    course_form = CourseForm()
    if course_form.validate_on_submit():
        course = Course(
            class_num = course_form.class_num.data,
            course_name = course_form.course_name.data,
        )
        db.session.add(course)
        db.session.commit()
        return render_template("admin/admin.html", message="courseテーブルに保存しました")
    course_list = db.session.query(Course).all()
    return render_template("admin/course.html", course_form=course_form, course_list=course_list)

@admin.route("/course/delete")
def course_delete():
    aaa = db.session.query(Course).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")

@admin.route("/subject", methods=["GET", "POST"])
def subject():
    subject_form = SubjectForm()
    courses = db.session.query(Course).all()
    names = set((c.course_name)for c in courses)
    subject_form.course_name.choices = [(c, c)for c in names]
    if subject_form.validate_on_submit():
        subject = Subject(
            subject_id = subject_form.subject_id.data,
            subject_name = subject_form.subject_name.data,
            course_name = subject_form.course_name.data
        )
        db.session.add(subject)
        db.session.commit()
        return render_template("admin/admin.html", message="subjectテーブルに保存しました")
    subject_list = db.session.query(Subject).all()
    return render_template("admin/subject.html", subject_form=subject_form, subject_list=subject_list)

@admin.route("/subject/delete")
def subject_delete():
    aaa = db.session.query(Subject).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")