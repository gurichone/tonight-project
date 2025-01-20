from app import db, mail # app.pyのdbをインポート
from .forms import TeacherLoginForm, TeacherSignUpForm, StudentLoginForm, StudentSignUpForm, EmailForm, OneTimeForm, NewPwForm # auth/forms.pyのTeacherLoginForm, TeacherSignUpForm, StudentLoginForm, StudentSignUpFormクラスを使えるようにする
from .models import Teacher, Student, School, ClassNum, Course, OneTime # auth/models.pyのTeacher, Student, School, ClassNum, Courseクラス(データベース)を使えるようにする
from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import datetime
import uuid
import hashlib

# authアプリを生成。テンプレートを保存するフォルダ名にtemplates、スタティックを保存するフォルダ名にstaticを指定
# htmlファイルを探すときは自動的にauth/templatesの中を参照するようになる
auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

# localhost:5000/auth/というURLが贈られてきたときの処理
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    teacherform = TeacherSignUpForm() # forms.pyのTeacherSignUpFormクラスを使えるようにする
    studentform = StudentSignUpForm() # forms.pyのStudentSignUpFormクラスを使えるようにする

    schools=db.session.query(School).all()
    studentform.student_school.choices=[(s.school_id, s.school_name)for s in schools]
    class_nums=db.session.query(ClassNum).all()
    studentform.student_class_num.choices=[(s.class_num, s.class_num)for s in class_nums]
    teacherform.teacher_class_num.choices=[(s.class_num, s.class_num)for s in class_nums]
    studentform.student_entrollment_year.choices=[(i, i)for i in range(datetime.datetime.now().year, 1900, -1)]
    # フォームが正しく入力されているかをチェックする
    if teacherform.validate_on_submit(): 
        # フォームが正しく入力されているときの処理
        teacher = Teacher(
            id=teacherform.teacher_id.data,
            teacher_name=teacherform.teacher_name.data, # DBのユーザーテーブルのusernameにフォームに入力されたユーザ名を代入
            teacher_email=teacherform.teacher_email.data, # DBのユーザーテーブルのemailにフォームに入力されたメールアドレスを代入
            password=teacherform.teacher_password.data, # DBのユーザーテーブルのpasswordにフォームに入力されたパスワードを代入
            class_num=teacherform.teacher_class_num.data,
            authority=teacherform.teacher_authority.data,
        )

        # メールアドレス重複チェックをする
        if teacher.is_duplicate_email():
            # メールアドレスが重複している場合
            flash("指定のメールアドレスは登録済みです") # htmlで表示するメッセージを追加
            return redirect(url_for("auth.signup")) # auth/views.pyのsignup関数を実行

        # DBにユーザー情報を登録する
        db.session.add(teacher)
        db.session.commit()

        return redirect(url_for("auth.login"))

        # フォームが正しく入力されているかをチェックする
    if studentform.validate_on_submit(): 
        # フォームが正しく入力されているときの処理
        course=db.session.query(ClassNum).filter_by(class_num=studentform.student_class_num.data).first()
        student = Student(
            id=studentform.student_id.data,
            student_name=studentform.student_name.data,
            student_email=studentform.student_email.data,
            password=studentform.student_password.data,
            entrollment_year=studentform.student_entrollment_year.data,
            birth_date=studentform.student_birth_date.data,
            school_id=studentform.student_school.data,
            course_id=course.course_id,
            class_num=studentform.student_class_num.data,
        )

        # メールアドレス重複チェックをする
        if student.is_duplicate_email():
            # メールアドレスが重複している場合
            flash("指定のメールアドレスは登録済みです") # htmlで表示するメッセージを追加
            return redirect(url_for("auth.signup")) # auth/views.pyのsignup関数を実行

        # DBにユーザー情報を登録する
        db.session.add(student)
        db.session.commit()

        return redirect(url_for("auth.login"))
    # フォームが正しく入力されていない場合はtemplates/auth/signup.htmlを表示
    return render_template("auth/signup.html", teacherform=teacherform, studentform=studentform)


# localhost:5000/login/というURLが送られてきたときの処理
@auth.route("/", methods=["GET", "POST"])
def login():
    teacherform = TeacherLoginForm() # forms.puのTeacherLoginFormを使えるようにする
    studentform = StudentLoginForm() # forms.puのStudentLoginFormを使えるようにする

    if teacherform.validate_on_submit():
        # 入力されたメールアドレスを持つユーザデータを取得
        teacher = Teacher.query.filter_by(id=teacherform.teacher_id.data).first() 

        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if teacher is not None and teacher.verify_password(teacherform.teacher_password.data):
            # ユーザ情報をセッションに登録
            login_user(teacher)
            # crud/templates/crud/index.htmlを表示
            return redirect(url_for("teacher.menu.t_menu"))

        flash("メールアドレスかパスワードか不正です") # ログイン失敗メッセージを設定する
    
    if studentform.validate_on_submit():
        # 入力されたメールアドレスを持つユーザデータを取得
        student = Student.query.filter_by(id=studentform.student_id.data).first() 

        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if student is not None and student.verify_password(studentform.student_password.data):
            # ユーザ情報をセッションに登録
            login_user(student)
            # crud/templates/crud/index.htmlを表示
            return redirect(url_for("student.menu.s_menu"))

        flash("メールアドレスかパスワードか不正です") # ログイン失敗メッセージを設定する

    return render_template("auth/login.html", teacherform=teacherform, studentform=studentform) # フォームが正しく入力されていなければauth/login.htmlを表示


# localhost:5000/logout/というURLが送られてきたときの処理
@auth.route("/logout")
def logout():
    logout_user() # ログアウト処理
    return redirect(url_for("auth.login")) # auth/views.pyのlogin関数を実行

@auth.route("/index")
# @login_required
def index():
    return render_template("auth/reset_done.html")

@auth.route("/delete")
def delete():
    aaa = db.session.query(Teacher).delete()
    aaa = db.session.query(Student  ).delete()
    db.session.commit()
    return "なにもなくなった"

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template("auth/" + template + ".txt", **kwargs)
    msg.html = render_template("auth/" + template + ".html", **kwargs)
    mail.send(msg)

@auth.route("/reset", methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        exist = False
        if len(form.id.data) == 6:
            teacher = db.session.query(Teacher).filter_by(id=form.id.data, teacher_email=form.mail.data).first()
            if teacher:
                user_id=teacher.id
                username=teacher.teacher_name
                exist = True
        if len(form.id.data) == 7:
            student = db.session.query(Student).filter_by(id=form.id.data, student_email=form.mail.data).first()
            if student:
                user_id=student.id
                username=student.student_name
                exist = True
        if exist:
            db.session.query(OneTime).filter_by(user_id=user_id).delete()
            db.session.commit()
            uu=str(uuid.uuid4())
            now=datetime.datetime.now()
            pw=user_id+str(now)
            pw_hash=hashlib.sha256(pw.encode()).hexdigest()
            onetime=OneTime(
                uu=uu,
                password=pw_hash[:6],
                user_id=user_id,
                time=now,
            )
            db.session.add(onetime)
            db.session.commit()
            session["onetime"] = uu
            send_email(form.mail.data, "EduEaseワンタイムパスワード", "onetime_email", username=username, password=pw_hash[:6])
        return redirect(url_for('auth.onetime'))
    return render_template("auth/reset.html", form=form)

@auth.route("/onetime", methods=["GET", "POST"])
def onetime():
    form = OneTimeForm()
    if form.validate_on_submit():
        onetime=db.session.query(OneTime).filter_by(uu=session["onetime"]).first()
        if onetime is not None and onetime.verify_password(form.onetime.data):
            td = datetime.datetime.now() - onetime.time
            if td.total_seconds() < 600:
                session.pop("onetime", None)
                session["user_id"]=onetime.user_id
                return redirect(url_for("auth.newpw"))
    return render_template("auth/onetime.html", form=form)

@auth.route("/newpw", methods=["GET", "POST"])
def newpw():
    form = NewPwForm()
    message=False
    if form.validate_on_submit():
        if form.password1.data == form.password2.data:
            user_id=session["user_id"]
            if len(user_id) == 6:
                teacher = db.session.query(Teacher).filter_by(id=user_id).first()
                teacher.password=form.password1.data
                db.session.add(teacher)
                db.session.commit()
            if len(user_id) == 7:
                student = db.session.query(Student).filter_by(id=user_id).first()
                student.password=form.password1.data
                db.session.add(student)
                db.session.commit()
            session.pop("user_id", None)
            return render_template("auth/reset_done.html")
        else:
            message="新しいパスワードの値が再確認で入力された値と違います"
    return render_template("auth/newpw.html", form=form, message=message)