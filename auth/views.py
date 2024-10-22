from app import db # app.pyのdbをインポート
from auth.forms import TeacherLoginForm, TeacherSignUpForm, StudentLoginForm, StudentSignUpForm # auth/forms.pyのTeacherLoginForm, TeacherSignUpForm, StudentLoginForm, StudentSignUpFormクラスを使えるようにする
from auth.models import Teacher, Student # auth/models.pyのTeacher, Studentクラス(データベース)を使えるようにする
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user

# authアプリを生成。テンプレートを保存するフォルダ名にtemplates、スタティックを保存するフォルダ名にstaticを指定
# htmlファイルを探すときは自動的にauth/templatesの中を参照するようになる
auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")

# localhost:5000/auth/というURLが贈られてきたときの処理
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    teacherform = TeacherSignUpForm() # forms.pyのTeacherSignUpFormクラスを使えるようにする
    studentform = StudentSignUpForm() # forms.pyのStudentSignUpFormクラスを使えるようにする

    # フォームが正しく入力されているかをチェックする
    if teacherform.validate_on_submit(): 
        # フォームが正しく入力されているときの処理
        teacher = Teacher(
            teacher_num=int(teacherform.teacher_num.data),
            class_num=teacherform.class_num.data,
            teacher_name=teacherform.teacher_name.data, # DBのユーザーテーブルのusernameにフォームに入力されたユーザ名を代入
            teacher_email=teacherform.email.data, # DBのユーザーテーブルのemailにフォームに入力されたメールアドレスを代入
            password=teacherform.password.data, # DBのユーザーテーブルのpasswordにフォームに入力されたパスワードを代入
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
        student = Student(
            student_num=studentform.student_num.data,
            class_num=studentform.class_num.data,
            student_name=studentform.student_name.data, # DBのユーザーテーブルのusernameにフォームに入力されたユーザ名を代入
            student_email=studentform.email.data, # DBのユーザーテーブルのemailにフォームに入力されたメールアドレスを代入
            password=studentform.password.data, # DBのユーザーテーブルのpasswordにフォームに入力されたパスワードを代入
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
        teacher = Teacher.query.filter_by(teacher_num=int(teacherform.teacher_num.data)).first() 

        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if teacher is not None and teacher.verify_password(teacherform.password.data):
            # ユーザ情報をセッションに登録
            login_user(teacher)
            # crud/templates/crud/index.htmlを表示
            return redirect(url_for("auth.index"))

        flash("メールアドレスかパスワードか不正です") # ログイン失敗メッセージを設定する
    
    if studentform.validate_on_submit():
        # 入力されたメールアドレスを持つユーザデータを取得
        student = Student.query.filter_by(student_num=int(studentform.student_num.data)).first() 

        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if student is not None and student.verify_password(studentform.password.data):
            # ユーザ情報をセッションに登録
            login_user(student)
            # crud/templates/crud/index.htmlを表示
            return redirect(url_for("auth.index"))

        flash("メールアドレスかパスワードか不正です") # ログイン失敗メッセージを設定する

    return render_template("auth/login.html", teacherform=teacherform, studentform=studentform) # フォームが正しく入力されていなければauth/login.htmlを表示


# localhost:5000/logout/というURLが送られてきたときの処理
@auth.route("/logout")
def logout():
    logout_user() # ログアウト処理
    return redirect(url_for("currydar.currydar_app")) # auth/views.pyのlogin関数を実行

@auth.route("/index")
def index():
    return render_template("auth/index.html")

@auth.route("/delete")
def delete():
    aaa = db.session.query(Teacher).delete()
    aaa = db.session.query(Student  ).delete()
    db.session.commit()
    return "なにもなくなった"