from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from teacher_seiseki.forms import SearchScore, AddScore, AttendScore, EditScore
from teacher_seiseki.models import Score
from auth.models import Student, Subject
from auth.models import Student
from datetime import datetime
from teacher_jikanwari.models import Timetable
import hashlib

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

    # 科目名を選択、テーブルのidに応じて科目名を表示している
    subjects = Subject.query.with_entities(Subject.subject_id, Subject.subject_name).all()
    score.subject_id.choices = [("","--")] + [(c.subject_id, c.subject_name)for c in subjects]

    # クラス番号を選択
    class_nums = Score.query.with_entities(Score.class_num).distinct().all()
    score.class_num.choices = [("","--")] + [(c.class_num, c.class_num)for c in class_nums]
    
    # ベースクエリの定義
    query = db.session.query(Score, Subject, Student).join(Subject, Score.subject_id == Subject.subject_id).join(Student, Score.id == Student.id)
    # 検索ボタンを押すとフィルタリング
    if score.validate_on_submit():
        subject_name = Subject.subject_name
        student_name = Student.student_name

        # 科目名、クラス番号、生徒番号のいずれかを入力しフィルターする
        if score.subject_id.data:
            query = query.filter(Score.subject_id == score.subject_id.data)
        if score.class_num.data:
            query = query.filter(Score.class_num == score.class_num.data)
        if score.student_name.data:
            query = query.filter(Student.student_name.like(f"%{score.student_name.data}%"))

        return render_template("/teacher_seiseki/index.html", score=score, subject_name=subject_name, student_name=student_name, results=query.all())

    # 検索が行われていない場合、全部の結果を表示
    return render_template("/teacher_seiseki/index.html", score=score, results=query.all())

# 成績画面の成績登録ボタンをクリックすると追加する画面を表示
@seiseki.route("/add", methods=["GET", "POST"])
def add():
    # フォームインスタンスを作成
    score_form = AddScore()

    # studentテーブル、subjectテーブルから情報を取得し、それぞれセレクトフィールドで表示する
    students = db.session.query(Student).all() 
    score_form.id.choices = [(c.id, c.id)for c in students]
    subjects = db.session.query(Subject).all()
    score_form.subject_id.choices = [(c.subject_id, c.subject_name)for c in subjects]
    
    # バリデートする際の変数actionの変化によって表示するものを変更する
    if score_form.validate_on_submit():
        action = request.form.get('action')
        # 
        if action == 'confirm':
            # 受け取ったフォームデータをそのまま表示する確認画面に移動
            student = db.session.query(Student).filter_by(id=score_form.id.data).first()
            student_name = student.student_name if student else "不明です"
            return render_template("teacher_seiseki/add.html", 
                                   score=score_form, student_name=student_name, confirm=True, success=False)

        elif action == 'add':
            # 重複チェックを実行
            existing_score = Score.query.filter_by(
                id = score_form.id.data,
                subject_id = score_form.subject_id.data,
            ).first()
            # エラー文を表示
            if existing_score:
                flash("同じ情報が既に登録されています。", "error")
                return render_template("teacher_seiseki/add.html",
                                       score=score_form,confirm=False,success=False)
            
            student = db.session.query(Student).filter_by(id=score_form.id.data).first()
            subject = db.session.query(Subject).filter_by(subject_id=score_form.subject_id.data).first()

            # フォームデータを使用してScoreモデルのインスタンスを作成し、データベースに登録
            score = Score(
                id=student.id,
                class_num=student.class_num,
                subject_id=subject.subject_id,
                assessment_id=score_form.assessment_id.data
            )
            db.session.add(score)
            db.session.commit()
            # 登録完了画面を表示する
            return render_template("teacher_seiseki/add.html", 
                                   score=score_form, student=student,subject=subject, confirm=False, success=True)
    # 最初は登録する情報を入力する画面に移る
    return render_template("teacher_seiseki/add.html", 
                           score=score_form, confirm=False, success=False)

# 出席日数を確認する画面を表示する
@seiseki.route("/attend", methods=["GET", "POST"])
def attend():
    # フォームインスタンスの作成
    attend = AttendScore()
    
    # 科目名を選択、テーブルのidに応じて科目名を表示している
    subjects = Subject.query.with_entities(Subject.subject_id, Subject.subject_name).all()
    attend.subject_id.choices = [("","--")] + [(c.subject_id, c.subject_name)for c in subjects]
    
    # クラス番号を選択
    class_nums = Score.query.with_entities(Score.class_num).distinct().all()
    attend.class_num.choices = [("","--")] + [(c.class_num, c.class_num)for c in class_nums]
    
    # ベースクエリの定義
    query = db.session.query(Score, Subject, Student).join(Subject, Score.subject_id == Subject.subject_id).join(Student, Score.id == Student.id)

    # フォームのバリデーションと検索条件の適用
    if attend.validate_on_submit():
        subject_name = Subject.subject_name
        student_name = Student.student_name

        # 科目名、クラス番号、生徒番号のいずれかを入力しフィルターする
        if attend.subject_id.data:
            query = query.filter(Score.subject_id == attend.subject_id.data)
        if attend.class_num.data:
            query = query.filter(Score.class_num == attend.class_num.data)
        if attend.student_name.data:
            query = query.filter(Score.student_name.like(f"%{attend.student_name.data}%"))

        # フィルタリング結果を取得し、画面に表示
        return render_template("/teacher_seiseki/attend.html", attend=attend, subject_name=subject_name, student_name=student_name, results=query.all())
    
    # 検索が行われていない場合、全部の結果を表示
    return render_template("/teacher_seiseki/attend.html", attend=attend, results=query.all())

# 成績の編集を行うための処理を実装
@seiseki.route("/edit/<int:score_id>", methods=["GET", "POST"])
def edit(score_id):

    # 成績を編集するフォームを作成(AddScoreの流用だが問題ない)
    form = EditScore()
    # score_idがまずあるかどうかの処理
    score = Score.query.filter(Score.score_id == score_id).first()
    if form.validate_on_submit():
        # edit.html内で編集ボタンを押下した際の処理
        score.assessment_id = form.assessment_id.data
        score.attend_day = form.attend_day.data
        db.session.commit()  # 変更を行い、更新
        flash("成績が正常に更新されました。", "success")
        return redirect(url_for("teacher.seiseki.search"))

    # 編集ボタンを押下してページに遷移した際の処理、ここで編集を行う
    student = Student.query.get(score.id)
    subject = Subject.query.get(score.subject_id)

    form.assessment_id.data = score.assessment_id
    form.attend_day.data = score.attend_day

    return render_template(
        "teacher_seiseki/edit.html",
        form=form,
        student=student,
        subject=subject,
        score=score
    )

# 成績の削除を行う処理の実装
@seiseki.route("/delete/<int:score_id>", methods=["POST"])
def delete(score_id):
    # 変数scoreでScoreテーブルのscore_idを取得
    score = Score.query.get(score_id)
    # ほぼidが存在するので消去する流れになる
    if score:
        db.session.delete(score)
        db.session.commit()
    # この処理はほぼ使われないだろうが一応書いておく
    else:
        flash("該当箇所が見つかりませんでした","error")
    # 他の画面には行かず、メニュー画面を表示する
    return redirect(url_for("teacher.seiseki.search"))

# 生徒の出席登録の際に発行するコードを先生側が用意するための処理の実装
@seiseki.route("/issue_code",methods=["GET","POST"])
def issue_code():
    # datetime関数で日時を取得
    now = datetime.now()
    year, month, day = now.year, now.month, now.day

    # 現在の日時に一致する時間割があるかどうかを検索
    timetable = db.session.query(Timetable).filter_by(year=year, month=month, day=day).first()

    # timetableが存在する場合の処理
    if timetable:
        if request.method == "POST":

            # 選択を終えコード発行ボタンを押下するとコードを発行し表示する。
            period = request.form.get("period")
            code_data = f"{timetable.id}{now.strftime('%Y%m%d%H%M%S')}{period}"
            code_hash = hashlib.sha256(code_data.encode()).hexdigest()[:6]
            return render_template("teacher_seiseki/display_code.html", code=code_hash)
        
        # 最初にTimetableから取得した授業一覧を表示する処理
        periods = [("period1", timetable.period1), ("period2", timetable.period2), ("period3", timetable.period3)]
        return render_template("teacher_seiseki/issue_code.html", periods=periods)
    
    # 存在しない場合はエラー文を表示する
    flash("本日、授業がないか登録されていません。","error")
    return redirect(url_for("teacher.seiseki.search"))