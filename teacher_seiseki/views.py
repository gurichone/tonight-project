from flask import Blueprint, render_template, redirect, url_for, request,flash
from app import db
from teacher_seiseki.forms import SearchScore, AddScore, AttendScore
from teacher_seiseki.models import Score
from auth.models import Student, ClassNum, Subject

seiseki = Blueprint(
    "seiseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 教員のメニュー画面にある成績ボタンを押すと生徒の成績を検索する欄が出てくる
@seiseki.route("/", methods=["GET", "POST"])
def search():
    # フォームインスタンスの作成
    score = SearchScore()
 
    # リストの取得
    results = Score.query.with_entities(
        Score.score_id,
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
    # 検索が行われていない場合、全部の結果を表示
    return render_template("/teacher_seiseki/index.html", score=score, results=results)

# 成績画面の成績登録ボタンをクリックすると追加する画面を表示
@seiseki.route("/add", methods=["GET", "POST"])
def add():
    # フォームインスタンスを作成
    score_form = AddScore()
    # バリデートする際の変数actionの変化によって表示するものを変更する
    if score_form.validate_on_submit():
        action = request.form.get('action')
        # 
        if action == 'confirm':
            # 受け取ったフォームデータをそのまま表示する確認画面に移動
            return render_template("teacher_seiseki/add.html", 
                                   score=score_form, confirm=True, success=False)

        elif action == 'add':
            # フォームデータを使用してScoreモデルのインスタンスを作成し、データベースに登録
            score = Score(
                student_num=score_form.student_num.data,
                student_name=score_form.student_name.data,
                subject_name=score_form.subject_name.data,
                assessment_id=score_form.assessment_id.data
            )
            db.session.add(score)
            db.session.commit()
            # 登録完了画面を表示する
            return render_template("teacher_seiseki/add.html", 
                                   score=score_form, confirm=False, success=True)
    # 最初は登録する情報を入力する画面に移る
    return render_template("teacher_seiseki/add.html", 
                           score=score_form, confirm=False, success=False)

# 出席日数を確認する画面を表示する
@seiseki.route("/attend", methods=["GET", "POST"])
def attend():
    # フォームインスタンスの作成
    attend = AttendScore()
    
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

        # フィルタリング結果を取得し、画面に表示
        results = query.all()
        return render_template("/teacher_seiseki/attend.html", attend=attend, results=results)
    # 検索が行われていない場合、全部の結果を表示
    return render_template("/teacher_seiseki/attend.html", attend=attend, results=results)

@seiseki.route("/delete/<int:score_id>", methods=["POST"])
def delete(score_id):
    score = Score.query.get(score_id)
    print(score.score_id)
    if score:
        db.session.delete(score)
        db.session.commit()
        flash("削除しました","success")
    else:
        flash("該当箇所が見つかりませんでした","error")
    return redirect(url_for("teacher.seiseki.search"))