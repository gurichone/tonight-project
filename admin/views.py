from flask import Blueprint, flash, redirect, render_template, request, url_for
from app import db 
from admin.forms import CourseForm, SubjectForm, ClassNumForm, CourseSubjectForm
from auth.models import Teacher, Student 
from teacher_teisyutsu.models import Subject, Course, ClassNum, CourseSubject

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@admin.route("/")
def admin_menu():
    return render_template("admin/admin.html", message="お前が管理者だ")

@admin.route("/course", methods=["GET", "POST"])
def course():
    course_form = CourseForm()
    if course_form.validate_on_submit():
        course = Course(
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
    if subject_form.validate_on_submit():
        subject = Subject(
            subject_name = subject_form.subject_name.data,
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

@admin.route("/cs", methods=["GET", "POST"])
def cs():
    form = CourseSubjectForm()

    # Courseテーブルから全取得
    courses = db.session.query(Course).all()

    # フォームのSelectField.choicesに設定
    form.course.choices = [(c.course_id, c.course_name)for c in courses]

    # Subjectテーブルから全取得
    subjects = db.session.query(Subject).all()

    # フォームのSelectField.choicesに設定
    form.subject.choices = [(s.subject_id, s.subject_name)for s in subjects]
    if form.validate_on_submit():
        cs = CourseSubject(
            subject_id = form.subject.data,
            course_id = form.course.data
        )
        db.session.add(cs)
        db.session.commit()
        return render_template("admin/admin.html", message="COURSE_SUBJECTテーブルに保存しました")
    cs_list = db.session.query(CourseSubject, Course, Subject).join(Course, CourseSubject.course_id==Course.course_id).join(Subject, CourseSubject.subject_id==Subject.subject_id).all()
    print("qwwqwq", cs_list)
    return render_template("admin/cs.html", form=form, cs_list=cs_list)

@admin.route("/cs/delete")
def cs_delete():
    aaa = db.session.query(CourseSubject).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")