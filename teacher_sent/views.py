from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from teacher_sent.forms import InformationForms
from teacher_sent.models import Information, Get_Information
from auth.models import Teacher, Student, ClassNum


sent = Blueprint(
    "sent",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@sent.route("/", methods=["GET", "POST"])
@login_required
# お知らせ送信
def teacher_sent():
    # 生徒が教員機能を使用できないようにする
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    
    form = InformationForms()

    # クラスの選択肢を動的に設定
    class_choices = [(c.class_num, f"クラス {c.class_num}") for c in db.session.query(ClassNum).all()]
    form.address.choices = class_choices

    if form.validate_on_submit():
        selected_class = form.address.data  # 選択されたクラス番号
        title = form.title.data
        discription = form.discription.data

        # Informationテーブルに新規情報を登録
        new_info = Information(
            title=title,
            discription=discription,
            teacher_num=current_user.id,
        )
        db.session.add(new_info)
        db.session.commit()

        # 選択されたクラスの生徒を取得し、Get_Informationに登録
        students = db.session.query(Student).filter_by(class_num=selected_class).all()
        for student in students:
            new_get_info = Get_Information(
                info_id=new_info.info_id,
                student_num=student.id,
                read=False,
            )
            db.session.add(new_get_info)

        db.session.commit()

        # 送信完了ページにリダイレクト
        return redirect(url_for("teacher.sent.teacher_sent_complete"))

    return render_template("teacher_sent/sent_form.html", form=form)

@sent.route("/complete")
@login_required
# 送信完了ページ
def teacher_sent_complete():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    return render_template("teacher_sent/sent_complete.html")
