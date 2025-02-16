from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db 
from admin.forms import CourseForm, SubjectForm, ClassNumForm, CourseSubjectForm, SchoolForm, StudentAddForm
from auth.models import Teacher, Student, Subject, Course, ClassNum, CourseSubject, School
from teacher_jikanwari.models import SubjectDetails
import datetime

admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")

@login_required
@admin.route("/")
def admin_menu():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    return render_template("admin/admin.html", message="管理者機能")
@login_required
@admin.route("/course", methods=["GET", "POST"])
def course():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
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
@login_required
@admin.route("/course/delete")
def course_delete():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    ccc = db.session.query(ClassNum).delete()
    bbb = db.session.query(CourseSubject).delete()
    aaa = db.session.query(Course).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")
@login_required
@admin.route("/subject", methods=["GET", "POST"])
def subject():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
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
@login_required
@admin.route("/subject/delete")
def subject_delete():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    bbb = db.session.query(CourseSubject).delete()
    aaa = db.session.query(Subject).delete()
    ccc = db.session.query(SubjectDetails).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")
@login_required
@admin.route("/school", methods=["GET", "POST"])
def school():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    school_form = SchoolForm()
    if school_form.validate_on_submit():
        school = School(
            school_name = school_form.school_name.data,
        )
        db.session.add(school)
        db.session.commit()
        return render_template("admin/admin.html", message="schoolテーブルに保存しました")
    school_list = db.session.query(School).all()
    return render_template("admin/school.html", school_form=school_form, school_list=school_list)
@login_required
@admin.route("/school/delete")
def school_delete():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    aaa = db.session.query(School).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")
@login_required
@admin.route("/cs", methods=["GET", "POST"])
def cs():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
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
    return render_template("admin/cs.html", form=form, cs_list=cs_list)
@login_required
@admin.route("/cs/delete")
def cs_delete():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    aaa = db.session.query(CourseSubject).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")
@login_required
@admin.route("/class", methods=["GET", "POST"])
def class_num():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    form = ClassNumForm()
    # Courseテーブルから全取得
    courses = db.session.query(Course).all()
    # フォームのSelectField.choicesに設定
    form.course.choices = [(c.course_id, c.course_name)for c in courses]
    if form.validate_on_submit():
        class_num = ClassNum(
            class_num = form.class_num.data,
            course_id = form.course.data
        )
        db.session.add(class_num)
        db.session.commit()
        return render_template("admin/admin.html", message="COURSE_SUBJECTテーブルに保存しました")
    class_list=db.session.query(ClassNum, Course).join(Course, ClassNum.course_id==Course.course_id).all()
    return render_template("admin/class.html", form=form, class_list=class_list)
@login_required
@admin.route("/class/delete")
def class_delete():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    if current_user.authority != 1:
        flash("管理者のみ利用可能な機能です")
        return redirect(url_for('teacher.menu.t_menu'))
    aaa = db.session.query(ClassNum).delete()
    db.session.commit()
    return render_template("admin/admin.html", message="けしたよ")

@admin.errorhandler(400)
@admin.errorhandler(404)
@admin.errorhandler(405)
@admin.errorhandler(500)
def error_handler(error):
    return render_template("admin/error.html", code=error.code, error=error)