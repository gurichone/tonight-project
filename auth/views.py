from app import db # app.pyのdbをインポート
from auth.forms import LoginForm, SignUpForm # auth/forms.pyのLoginForm, SignUpFormクラスを使えるようにする
from auth.models import User # crud/models.pyのUserクラスを使えるようにする
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

# authアプリを生成。テンプレートを保存するフォルダ名にtemplates、スタティックを保存するフォルダ名にstaticを指定
# htmlファイルを探すときは自動的にauth/templatesの中を参照するようになる
auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


# localhost:5000/auth/というURLが贈られてきたときの処理
@auth.route("/")
def index():
    return render_template("auth/index.html") # auth/index.htmlを表示

# localhost:5000/auth/というURLが贈られてきたときの処理
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm() # forms.pyのSignUpFormクラスを使えるようにする

    # フォームが正しく入力されているかをチェックする
    if form.validate_on_submit(): 
        # フォームが正しく入力されているときの処理
        user = User(
            username=form.username.data, # DBのユーザーテーブルのusernameにフォームに入力されたユーザ名を代入
            email=form.email.data, # DBのユーザーテーブルのemailにフォームに入力されたメールアドレスを代入
            password=form.password.data, # DBのユーザーテーブルのpasswordにフォームに入力されたパスワードを代入
        )

        # メールアドレス重複チェックをする
        if user.is_duplicate_email():
            # メールアドレスが重複している場合
            flash("指定のメールアドレスは登録済みです") # htmlで表示するメッセージを追加
            return redirect(url_for("auth.signup")) # auth/views.pyのsignup関数を実行

        # DBにユーザー情報を登録する
        db.session.add(user)
        db.session.commit()

        # ユーザー情報をセッションに格納する
        login_user(user)

        next_ = request.args.get("next")
        # サインアップ前に表示していたページがない場合index.htmlを表示
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("currydar.currydar_app")
        # サインアップの前にアクセスしていたページに遷移
        return redirect(next_)

    # フォームが正しく入力されていない場合はtemplates/auth/signup.htmlを表示
    return render_template("auth/signup.html", form=form)


# localhost:5000/login/というURLが送られてきたときの処理
@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm() # forms.puのLoginFormを使えるようにする

    if form.validate_on_submit():
        # 入力されたメールアドレスを持つユーザデータを取得
        user = User.query.filter_by(email=form.email.data).first() 

        # ユーザーが存在しパスワードが一致する場合はログインを許可する
        if user is not None and user.verify_password(form.password.data):
            # ユーザ情報をセッションに登録
            login_user(user)
            # crud/templates/crud/index.htmlを表示
            return redirect(url_for("currydar.currydar_app"))

        flash("メールアドレスかパスワードか不正です") # ログイン失敗メッセージを設定する
    return render_template("auth/login.html", form=form) # フォームが正しく入力されていなければauth/login.htmlを表示


# localhost:5000/logout/というURLが送られてきたときの処理
@auth.route("/logout")
def logout():
    logout_user() # ログアウト処理
    return redirect(url_for("currydar.currydar_app")) # auth/views.pyのlogin関数を実行