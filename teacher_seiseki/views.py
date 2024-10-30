from flask import Blueprint, render_template, redirect, url_for, request
from app import db
from teacher_seiseki.forms import SearchScore, AddScore
from teacher_seiseki.models import Score

seiseki = Blueprint(
    "seiseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 教員のメニュー画面にある成績ボタンを押すと生徒の成績を検索する欄が出てくる
@seiseki.route("/", methods=["GET", "POST"])
def search():
    score = SearchScore()
    # 科目名を選択する際の処理
    subject_names = db.session.query(Score).all()
    names = set((c.subject_name)for c in subject_names)
    score.subject_name.choices = [(c,c)for c in names]
    # クラス番号を選択する際の処理
    class_nums = db.session.query(Score).all()
    nums = set((c.class_num)for c in class_nums)
    score.class_num.choices = [(c,c)for c in nums]
    if score.validate_on_submit():
        # 科目名、クラス番号、生徒番号のいずれかを入力する
        score = Score(
            subject_name = score.subject_name.data,
            class_num = score.class_num.data,
            student_num = score.student_num.data,
        )
        # 検索結果を出力してhtmlに表示
        # db.session.
        return redirect(url_for("teacher.seiseki.search"))  
    return render_template("/teacher_seiseki/index.html",score=score)

# 成績画面の成績登録ボタンをクリックすると追加する画面を表示
@seiseki.route("/add", methods=["GET", "POST"])
def add():
    score = AddScore()
    if score.validate_on_submit():
        print("AAAAAAAAAAAAAAAAAAAAAA", score.student_num.data)
        # 生徒番号、氏名、科目名、評価を入力
        score = Score(
            student_num = score.student_num.data,
            student_name = score.student_name.data,
            subject_name = score.subject_name.data,
            assessment_id = score.assessment_id.data,
        )
        # データベースに登録
        db.session.add(score)
        db.session.commit
        return redirect(url_for("teacher.seiseki.add"))
    return render_template("/teacher_seiseki/add.html", score=score)

@seiseki.route("/attend", methods=["GET", "POST"])
def attend():
    return None