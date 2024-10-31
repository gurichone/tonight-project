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
@seiseki.route("/search", methods=["GET", "POST"])
def search():
    # フォームインスタンスの作成
    score = SearchScore()
    
    # リストの取得
    results = Score.query.with_entities(
        Score.subject_name,
        Score.class_num,
        Score.student_name,
        Score.assessment_id,
    ).all()
    # 科目名を選択する際の処理
    names = set(c.subject_name for c in results)
    score.subject_name.choices = [("", "ーー")] + [(c, c) for c in names]
    
    # クラス番号を選択する際の処理
    nums = set(c.class_num for c in results)
    score.class_num.choices = [("", "ーー")] + [(c, c) for c in nums]
    
    # ベースクエリの定義
    query = Score.query

    # フォームのバリデーションと検索条件の適用
    if score.validate_on_submit():
        # 科目名、クラス番号、生徒番号のいずれかを入力しフィルターする
        if score.subject_name.data:
            query = query.filter(Score.subject_name == score.subject_name.data)
        if score.class_num.data:
            query = query.filter(Score.class_num == score.class_num.data)
        if score.student_name.data:
            query = query.filter(Score.student_name.like(f"%{score.student_name.data}%"))

        # フィルタリング結果を取得
        results = query.all()
        return render_template("/teacher_seiseki/index.html", score=score, results=results)
    # 検索が行われていない場合、空の結果を表示
    return render_template("/teacher_seiseki/index.html", score=score, results=results)


# 成績画面の成績登録ボタンをクリックすると追加する画面を表示
@seiseki.route("/add", methods=["GET", "POST"])
def add():
    score = AddScore()
    if score.validate_on_submit():
        # 生徒番号、氏名、科目名、評価を入力
        score = Score(
            student_num = score.student_num.data,
            student_name = score.student_name.data,
            subject_name = score.subject_name.data,
            assessment_id = score.assessment_id.data,
        )
        # データベースに登録
        db.session.add(score)
        db.session.commit()
        return redirect(url_for("teacher.seiseki.add"))
    # htmlに表示
    return render_template("/teacher_seiseki/add.html", score=score)

@seiseki.route("/attend", methods=["GET", "POST"])
def attend():
    # フォームインスタンスの作成
    attend = SearchScore()
    
    # リストの取得
    results = Score.query.with_entities(
        Score.subject_name,
        Score.class_num,
        Score.student_name,
        Score.attend_day,
    ).all()
    # 科目名を選択する際の処理
    names = set(c.subject_name for c in results)
    attend.subject_name.choices = [("", "ーー")] + [(c, c) for c in names]
    
    # クラス番号を選択する際の処理
    nums = set(c.class_num for c in results)
    attend.class_num.choices = [("", "ーー")] + [(c, c) for c in nums]
    
    # ベースクエリの定義
    query = Score.query

    # フォームのバリデーションと検索条件の適用
    if attend.validate_on_submit():
        # 科目名、クラス番号、生徒番号のいずれかを入力しフィルターする
        if attend.subject_name.data:
            query = query.filter(Score.subject_name == attend.subject_name.data)
        if attend.class_num.data:
            query = query.filter(Score.class_num == attend.class_num.data)
        if attend.student_name.data:
            query = query.filter(Score.student_name.like(f"%{attend.student_name.data}%"))

        # フィルタリング結果を取得
        results = query.all()
        return render_template("/teacher_seiseki/attend.html", attend=attend, results=results)
    # 検索が行われていない場合、空の結果を表示
    return render_template("/teacher_seiseki/attend.html", attend=attend, results=results)