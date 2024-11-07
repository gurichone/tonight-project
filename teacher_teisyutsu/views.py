from flask import Blueprint, render_template, redirect, url_for, session, current_app
from flask_login import current_user, login_required
from wtforms.validators import ReadOnly
from app import db
from teacher_teisyutsu.forms import SubmissionForms, CreateSubmissionForms
from teacher_teisyutsu.models import Submission, Personal_Submission
from auth.models import Subject, Course, Teacher, Student, CourseSubject, ClassNum
import os
import shutil
from pathlib import Path

teisyutsu = Blueprint(
    "teisyutsu",
    __name__,
    template_folder="templates",
    static_folder="static",
)
# メインメニュー
@teisyutsu.route("/", methods=["GET", "POST"])
@login_required
def t_teisyutsu():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    form = SubmissionForms()
    # 科目の選択肢をデータベースから取得
    course =db.session.query(ClassNum).filter_by(class_num=current_user.class_num).first()
    subjects = db.session.query(Subject, CourseSubject).join(CourseSubject, CourseSubject.subject_id==Subject.subject_id).filter_by(course_id=course.course_id).all()
    form.subject.choices=[(0, "指定なし")]+[(s.Subject.subject_id, s.Subject.subject_name)for s in subjects]
    if form.validate_on_submit():
        # filter_byにformの入力内容を追加
        submissions = db.session.query(Submission, Subject).join(Submission,Submission.subject_id==Subject.subject_id).filter_by(class_num = current_user.class_num)
        if form.subject.data:
            submissions = submissions.filter_by(subject_id=form.subject.data)
        if form.type.data:
            submissions = submissions.filter_by(submission_type=form.type.data)
        submissions = submissions.all()
        # 選択した科目をsubjectとして送る
        return render_template("teacher_teisyutsu/admin.html", submissions=submissions, form=form, subject=db.session.query(Subject).filter_by(subject_id = form.subject.data).first())
    # ログインしているユーザーのクラスで絞る
    submissions = db.session.query(Submission, Subject).join(Submission,Submission.subject_id==Subject.subject_id).filter_by(class_num = current_user.class_num).all()
    return render_template("teacher_teisyutsu/admin.html", submissions=submissions, form=form)
# 追加
@teisyutsu.route("/add", methods=["GET", "POST"])
@login_required
def t_teisyutsu_add():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    form1 = CreateSubmissionForms()
    # 科目の選択肢をデータベースから取得
    course =db.session.query(ClassNum).filter_by(class_num=current_user.class_num).first()
    subjects = db.session.query(Subject, CourseSubject).join(CourseSubject, CourseSubject.subject_id==Subject.subject_id).filter_by(course_id=course.course_id).all()
    form1.subject.choices=[(s.Subject.subject_id, s.Subject.subject_name)for s in subjects]
    if form1.validate_on_submit():
        # もう一つのフォームにデータを移す(入力内容確認の準備)
        form2 = CreateSubmissionForms()
        s = db.session.query(Subject).filter_by(subject_id = form1.subject.data).first()
        form2.name.data=form1.name.data
        form2.subject.choices=[(s.subject_id, s.subject_name)]
        form2.type.choices=[form2.type.choices[form1.type.data]]
        form2.rimit.data=form1.rimit.data
        form2.scoring_type.choices=[form2.scoring_type.choices[form1.scoring_type.data]]
        form2.question.data=form1.question.data
        form2.testcase.data=form1.testcase.data
        # 入力内容確認画面を表示
        return render_template("teacher_teisyutsu/confirmation.html", form=form2)
    # 追加画面
    return render_template("teacher_teisyutsu/add.html", form=form1)

@teisyutsu.route("/confirmation", methods=["GET", "POST"])
@login_required
def t_teisyutsu_confirmation():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    form2 = CreateSubmissionForms()
    course =db.session.query(ClassNum).filter_by(class_num=current_user.class_num).first()
    subjects = db.session.query(Subject, CourseSubject).join(CourseSubject, CourseSubject.subject_id==Subject.subject_id).filter_by(course_id=course.course_id).all()
    form2.subject.choices=[(s.Subject.subject_id, s.Subject.subject_name)for s in subjects]
    if form2.validate_on_submit():
        # データベースに保存
        submission = Submission(
            submission_name = form2.name.data,
            subject_id = form2.subject.data,
            class_num = current_user.class_num,
            submission_type = form2.type.data,
            submission_rimit = form2.rimit.data,
            scoring_type = form2.scoring_type.data,
            question = form2.question.data,
            testcase = form2.testcase.data
        )
        db.session.add(submission)
        db.session.commit()
        # 個人の提出物データを作成
        # ログインユーザーのクラスの生徒を取得
        students=db.session.query(Student).filter_by(class_num = current_user.class_num).all()
        # 元データと個人用データのidをセットとして取得し個人用データに存在しないものをadd_idにいれる
        origin_id={i.submission_id for i in db.session.query(Submission).all()}
        personal_id={i.submission_id for i in db.session.query(Personal_Submission).all()}
        add_id=origin_id-personal_id
        personal = list()
        # 個人のデータを保存
        for i in add_id:
            os.mkdir(Path(current_app.config["SUBMIT_FOLDER"], str(i)))
            for s in students:
                personal.append(Personal_Submission(
                    submission_id=i,
                    student_id=s.id,
                ))
                db.session.add(personal[-1])
                db.session.commit()
        
        return render_template("teacher_teisyutsu/add_done.html")
    # return redirect(url_for("teacher.teisyutsu.t_teisyutsu"))
    return render_template("teacher_teisyutsu/confirmation.html", form=form2)
    


@teisyutsu.route("/edit/<submission_id>", methods=["GET", "POST"])
@login_required
def t_teisyutsu_edit(submission_id):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    session["submission"]=submission_id
    form1 = CreateSubmissionForms()
    submission=db.session.query(Submission).filter_by(submission_id=submission_id).first()
    course =db.session.query(ClassNum).filter_by(class_num=current_user.class_num).first()
    subjects = db.session.query(Subject, CourseSubject).join(CourseSubject, CourseSubject.subject_id==Subject.subject_id).filter_by(course_id=course.course_id).all()
    subjects=[(s.Subject.subject_id, s.Subject.subject_name)for s in subjects]
    for i in range(len(subjects)):
        if subjects[i][0] == submission.subject_id:
            subjects[0], subjects[i] = subjects[i], subjects[0]
    form1.subject.choices=subjects
    # 科目の選択肢をデータベースから取得
    if form1.validate_on_submit():
        # もう一つのフォームにデータを移す(入力内容確認の準備)
        form2 = CreateSubmissionForms()
        s = db.session.query(Subject).filter_by(subject_id = form1.subject.data).first()
        form2.name.data=form1.name.data
        form2.subject.choices=[(s.subject_id, s.subject_name)]
        form2.type.choices=[form2.type.choices[form1.type.data]]
        form2.rimit.data=form1.rimit.data
        form2.scoring_type.choices=[form2.scoring_type.choices[form1.scoring_type.data]]
        form2.question.data=form1.question.data
        form2.testcase.data=form1.testcase.data
        # 入力内容確認画面を表示
        return render_template("teacher_teisyutsu/edit_confirm.html", form=form2)
    # 編集画面
    form1.name.data=submission.submission_name
    for i in range(len(form1.type.choices)):
        if form1.type.choices[i][0] == submission.submission_type:
            form1.type.choices[0], form1.type.choices[i] = form1.type.choices[i], form1.type.choices[0]
    form1.rimit.data=submission.submission_rimit
    for i in range(len(form1.scoring_type.choices)):
        if form1.scoring_type.choices[i][0] == submission.scoring_type:
            form1.scoring_type.choices[0], form1.scoring_type.choices[i] = form1.scoring_type.choices[i], form1.scoring_type.choices[0]
    form1.question.data=submission.question
    form1.testcase.data=submission.testcase

    return render_template("teacher_teisyutsu/edit.html", form=form1, submission_id=submission_id)

@teisyutsu.route("/confirm_edit", methods=["GET", "POST"])
@login_required
def t_teisyutsu_confirm_edit():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    form2 = CreateSubmissionForms()
    subjects = db.session.query(Subject).all()
    form2.subject.choices=[(s.subject_id, s.subject_name)for s in subjects]
    if form2.validate_on_submit():
        submission_id=session["submission"]
        # データベースに保存
        submission = db.session.query(Submission).filter_by(submission_id=submission_id).first()
        submission.submission_name = form2.name.data
        submission.subject_id = form2.subject.data
        submission.class_num = current_user.class_num
        submission.submission_type = form2.type.data
        submission.submission_rimit = form2.rimit.data
        submission.scoring_type = form2.scoring_type.data
        submission.question = form2.question.data
        submission.testcase = form2.testcase.data
        
        db.session.add(submission)
        db.session.commit()
        
        return render_template("teacher_teisyutsu/edit_done.html")
    # return redirect(url_for("teacher.teisyutsu.t_teisyutsu"))
    return render_template("teacher_teisyutsu/confirmation.html", form=form2)

@teisyutsu.route("/delete/<submission_id>", methods=["GET", "POST"])
@login_required
def t_teisyutsu_delete(submission_id):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission = db.session.query(Submission).filter_by(submission_id=submission_id).first()
    session["submission"] = submission.submission_id
    return render_template("teacher_teisyutsu/delete.html", submission=submission.submission_name)

@teisyutsu.route("/delete_done", methods=["GET", "POST"])
@login_required
def t_teisyutsu_delete_done():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission=session["submission"]
    db.session.query(Personal_Submission).filter_by(submission_id=submission).delete()
    db.session.query(Submission).filter_by(submission_id=submission).delete()
    db.session.commit()
    shutil.rmtree(Path(current_app.config["SUBMIT_FOLDER"], str(submission)))
    return render_template("teacher_teisyutsu/delete_done.html")