from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import current_user, login_required
from app import db
from teacher_seiseki.forms import SearchScore, AddScore, AttendScore, EditScore
from teacher_seiseki.models import Score, Syusseki
from auth.models import Student, Subject, CourseSubject, ClassNum, Student
from datetime import datetime,timedelta
from teacher_jikanwari.models import Timetable
import hashlib
from sqlalchemy import or_

seiseki = Blueprint(
    "seiseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 教員のメニュー画面にある成績ボタンを押すと生徒の成績を検索する欄が出てくる
@seiseki.route("/", methods=["GET", "POST"])
@login_required
def search():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")

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

    # 下記のコードでデータベースに情報を無作為に追加できる
    # print("joinつかうやつ", query.all())
    # mori = db.session.query(Score).filter_by(class_num="1-71").first()
    # mori.id="2384849"
    # db.session.add(mori)
    # haru = db.session.query(Score).filter_by(class_num="1-72").first()
    # haru.id="2384850"
    # db.session.add(haru)
    # db.session.commit()
    
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

        return render_template(
            "/teacher_seiseki/index.html",
            score=score,
            subject_name=subject_name,
            student_name=student_name,
            results=query.all()
            )
    # 検索が行われていない場合、全部の結果を表示
    return render_template("/teacher_seiseki/index.html", score=score, results=query.all())

# 成績画面の成績登録ボタンをクリックすると追加する画面を表示
@seiseki.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    # フォームインスタンスを作成
    score_form = AddScore()

    # studentテーブル、subjectテーブルから情報を取得し、それぞれセレクトフィールドで表示する
    students = db.session.query(Student).filter_by(class_num = current_user.class_num).all() 
    score_form.id.choices = [(c.id, c.id)for c in students]
    course =db.session.query(ClassNum).filter_by(class_num=current_user.class_num).first()
    subjects = db.session.query(Subject, CourseSubject).join(CourseSubject, CourseSubject.subject_id==Subject.subject_id).filter_by(course_id=course.course_id).all()
    score_form.subject_id.choices = [(c.Subject.subject_id, c.Subject.subject_name)for c in subjects]
    
    # バリデートする際の変数actionの変化によって表示するものを変更する
    if score_form.validate_on_submit():
        action = request.form.get('action')
        # 
        if action == 'confirm':
            # 受け取ったフォームデータをそのまま表示する確認画面に移動
            student = db.session.query(Student).filter_by(id=score_form.id.data).first()
            student_name = student.student_name if student else "不明です"
            return render_template(
                "teacher_seiseki/add.html", 
                score=score_form,
                student_name=student_name,
                confirm=True,
                success=False
                )

        elif action == 'add':
            # 重複チェックを実行
            existing_score = Score.query.filter_by(
                id = score_form.id.data,
                subject_id = score_form.subject_id.data,
            ).first()
            # エラー文を表示
            if existing_score:
                if existing_score.assessment_id is not None:
                    flash("同じ情報が既に登録されています。", "error")
                    return render_template(
                        "teacher_seiseki/add.html",
                        score=score_form,
                        confirm=False,
                        success=False
                        )
                else:
                    student = db.session.query(Student).filter_by(id=score_form.id.data).first()
                    subject = db.session.query(Subject).filter_by(subject_id=score_form.subject_id.data).first()

                    # フォームデータを使用してScoreモデルのインスタンスを作成し、データベースに登録
                    existing_score.assessment_id=score_form.assessment_id.data
                    
                    db.session.add(existing_score)
                    db.session.commit()
            else:
            
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
            return render_template(
                "teacher_seiseki/add.html", 
                score=score_form, 
                student=student,
                subject=subject,
                confirm=False, 
                success=True
                )
    # 最初は登録する情報を入力する画面に移る
    return render_template(
        "teacher_seiseki/add.html", 
        score=score_form, 
        confirm=False, 
        success=False
        )

# 出席日数を確認する画面を表示する
@seiseki.route("/attend", methods=["GET", "POST"])
@login_required
def attend():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    # フォームインスタンスの作成
    attend = AttendScore()
    now = datetime.now()
    # クラス番号を選択
    student_name = Student.query.filter_by(class_num=current_user.class_num).with_entities(Student.id, Student.student_name).all()
    attend.student_name.choices = [(s.id, "{}({})".format(s.student_name, s.id))for s in student_name]
    
    attend.year.choices = [(now.year-1, now.year-1), (now.year, now.year), (now.year+1, now.year+1)]
    attend.month.choices = [(i, i)for i in range(1,13)]

    # フォームのバリデーションと検索条件の適用
    if attend.validate_on_submit():
        # subject_name = Subject.subject_name
        # student_name = Student.student_name

        
        
        selected_year = attend.year.data
        selected_month = attend.month.data

        syusseki = [[s.day, s.periods] for s in db.session.query(Syusseki).filter_by(student_id=attend.student_name.data, year=selected_year, month=selected_month).all()]
        print(syusseki)
        # 年月を指定してJikanwariエントリを取得
        entries = Timetable.query.filter_by(year=selected_year, month=selected_month, class_num=current_user.class_num).all()
        sbj_key_val = {subject.subject_id:subject.subject_name for subject in db.session.query(Subject).all()}
        # フィルタリング結果を取得し、画面に表示 
        print(attend.year.data, attend.month.data)
        return render_template(
            "/teacher_seiseki/attend.html", 
            attend=attend, 
            # subject_name=subject_name, 
            # student_name=student_name, 
            # year=selected_year,
            # month=selected_month,
            results=True,
            entries=entries,
            sbj_key_val=sbj_key_val,
            thisyear = now.year,
            syusseki=syusseki
            )
    
    # 検索が行われていない場合、何も表示しない
    attend.year.data = now.year
    attend.month.data = now.month
    return render_template(
        "/teacher_seiseki/attend.html", 
        attend=attend,
        results=False,
        thisyear = now.year
        )
@seiseki.route("/attend_add/<attend_info>", methods=["GET", "POST"])
@login_required
def attend_add(attend_info):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    
    attend_info = attend_info[1:-1].split(", ")
    # print(attend_info[0], attend_info[1], attend_info[2], attend_info[3], attend_info[4], attend_info[5])
    syusseki = Syusseki(
        year=int(attend_info[0]), 
        month=int(attend_info[1]), 
        day=int(attend_info[2]), 
        periods=int(attend_info[3]), 
        student_id=attend_info[4][1:-1]
    )
    db.session.add(syusseki)
    db.session.commit()
    score = db.session.query(Score).filter_by(id=attend_info[4][1:-1], subject_id=int(attend_info[5])).first()
    # print(attend_info[4][1:-1],int(attend_info[5]))
    if score is not None:
        if score.attend_day is None:
            score.attend_day = 1
            db.session.add(score)
            db.session.commit()
        else:
            score.attend_day += 1
            db.session.add(score)
            db.session.commit()
    else:
        score = Score(
            id=attend_info[4][1:-1],
            class_num=current_user.class_num,
            subject_id=int(attend_info[5]),
            attend_day = 1
        )
        db.session.add(score)
        db.session.commit()
    # フォームインスタンスの作成
    attend = AttendScore()
    now = datetime.now()
    
    # クラス番号を選択
    student_name = Student.query.filter_by(class_num=current_user.class_num).with_entities(Student.id, Student.student_name).all()
    attend.student_name.choices = [(s.id, "{}({})".format(s.student_name, s.id))for s in student_name]
    
    attend.year.choices = [(now.year-1, now.year-1), (now.year, now.year), (now.year+1, now.year+1)]
    attend.month.choices = [(i, i)for i in range(1,13)]

    attend.year.data = int(attend_info[0])
    attend.month.data = int(attend_info[1])
    attend.student_name.data = attend_info[4][1:-1]
    selected_year = attend.year.data
    selected_month = attend.month.data

    syusseki = [[s.day, s.periods] for s in db.session.query(Syusseki).filter_by(student_id=attend.student_name.data, year=selected_year, month=selected_month).all()]
    # print(syusseki)
    # 年月を指定してJikanwariエントリを取得
    entries = Timetable.query.filter_by(year=selected_year, month=selected_month, class_num=current_user.class_num).all()
    sbj_key_val = {subject.subject_id:subject.subject_name for subject in db.session.query(Subject).all()}
    # フィルタリング結果を取得し、画面に表示 
    return render_template(
        "/teacher_seiseki/attend.html", 
        attend=attend, 
        # subject_name=subject_name, 
        # student_name=student_name, 
        # year=selected_year,
        # month=selected_month,
        results=True,
        entries=entries,
        sbj_key_val=sbj_key_val,
        thisyear = now.year,
        syusseki=syusseki
        )
@seiseki.route("/attend_delete/<attend_info>", methods=["GET", "POST"])
@login_required
def attend_delete(attend_info):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    attend_info = attend_info[1:-1].split(", ")
    print(attend_info[0], attend_info[1], attend_info[2], attend_info[3], attend_info[4])

    aaa = db.session.query(Syusseki).filter_by(year=int(attend_info[0]), month=int(attend_info[1]), day=int(attend_info[2]), periods=int(attend_info[3]), student_id=attend_info[4][1:-1]).delete()
    db.session.commit()
    score = db.session.query(Score).filter_by(id=attend_info[4][1:-1], subject_id=int(attend_info[5])).first()
    score.attend_day -= 1
    db.session.add(score)
    db.session.commit()
    # フォームインスタンスの作成
    attend = AttendScore()
    now = datetime.now()
    
    # クラス番号を選択
    student_name = Student.query.filter_by(class_num=current_user.class_num).with_entities(Student.id, Student.student_name).all()
    attend.student_name.choices = [(s.id, "{}({})".format(s.student_name, s.id))for s in student_name]
    
    attend.year.choices = [(now.year-1, now.year-1), (now.year, now.year), (now.year+1, now.year+1)]
    attend.month.choices = [(i, i)for i in range(1,13)]

    attend.year.data = int(attend_info[0])
    attend.month.data = int(attend_info[1])
    attend.student_name.data = attend_info[4][1:-1]
    selected_year = attend.year.data
    selected_month = attend.month.data

    syusseki = [[s.day, s.periods] for s in db.session.query(Syusseki).filter_by(student_id=attend.student_name.data, year=selected_year, month=selected_month).all()]
    print(syusseki)
    # 年月を指定してJikanwariエントリを取得
    entries = Timetable.query.filter_by(year=selected_year, month=selected_month, class_num=current_user.class_num).all()
    sbj_key_val = {subject.subject_id:subject.subject_name for subject in db.session.query(Subject).all()}
    # フィルタリング結果を取得し、画面に表示 
    return render_template(
        "/teacher_seiseki/attend.html", 
        attend=attend, 
        # subject_name=subject_name, 
        # student_name=student_name, 
        # year=selected_year,
        # month=selected_month,
        results=True,
        entries=entries,
        sbj_key_val=sbj_key_val,
        thisyear = now.year,
        syusseki=syusseki
        )

# 成績の編集を行うための処理を実装
@seiseki.route("/edit/<int:score_id>", methods=["GET", "POST"])
@login_required
def edit(score_id):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")

    # 成績を編集するフォームを作成(AddScoreの流用だが問題ない)
    form = EditScore()
    # score_idがまずあるかどうかの処理
    score = Score.query.filter(Score.score_id == score_id).first()
    if form.validate_on_submit():
        # edit.html内で編集ボタンを押下した際の処理
        score.assessment_id = form.assessment_id.data
        score.attend_day = form.attend_day.data
        db.session.commit()  # 変更を行い、更新
        return render_template("teacher_seiseki/edit_complete.html",form=form)

    # 編集ボタンを押下してページに遷移した際の処理、ここで編集を行う
    student = Student.query.get(score.id)
    subject = Subject.query.get(score.subject_id)

    form.assessment_id.data = score.assessment_id
    syusseki = db.session.query(Syusseki).filter_by(student_id=score.id).all()
    attend_day = 0
    for s in syusseki:
        
        timetable =db.session.query(Timetable).filter_by(class_num = current_user.class_num, year=s.year, month=s.month, day=s.day).first()
        # print(s.periods, "----------------------------", timetable.period1, timetable.period2, timetable.period3, "---------", score.subject_id)
        if s.periods == 1:
            if timetable.period1 == int(score.subject_id):
                attend_day += 1
        elif s.periods == 2:
            if timetable.period2 == int(score.subject_id):
                attend_day += 1
        elif s.periods == 3:
            if timetable.period3 == int(score.subject_id):
                attend_day += 1

    form.attend_day.data = attend_day

    return render_template(
        "teacher_seiseki/edit.html",
        form=form,
        student=student,
        subject=subject,
        score=score
    )

# 成績の削除を行う処理の実装
@seiseki.route("/delete/<int:score_id>", methods=["POST"])
@login_required
def delete(score_id):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
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

@seiseki.route("/issue_code", methods=["GET", "POST"])
@login_required
def issue_code():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    
    # セッションの期限切れチェックと削除処理
    # if 'code_timestamp' in session:
    #     code_time = datetime.fromtimestamp(session['code_timestamp'])
    #     if datetime.now() - code_time > timedelta(minutes=5):
    #         session.pop('attendance_code', None)
    #         session.pop('code_timestamp', None)

    # datetime関数で日時を取得
    now = datetime.now()
    year, month, day = now.year, now.month, now.day

    # 現在の日時に一致する時間割があるかどうかを検索
    # timetable = db.session.query(Timetable).filter_by(year=year, month=month, day=day).first()


    if request.method == "POST":
        period = request.form.get("period")

        print("\n\n", period)

        # timetable = (
        #     db.session.query(Timetable)
        #     .filter_by(year=year, month=month, day=day)
        #     .filter(or_(Timetable.period1 == period, Timetable.period2 == period, Timetable.period3 == period))
        #     .first()
        # )

        # `subject`テーブルに`period`で指定された科目が存在するか確認
        # subject_name = getattr(timetable, f"period{period}", None)
        # subject = db.session.query(Subject).filter(Subject.subject_name == period).first()

        # if timetable and subject:
        # コードを発行し表示する
        code_data = f"{now.strftime('%Y%m%d')}{period}" + "jn;zsbvuo;bbh;rlznnzibvnbrnl.fbk;lnk.szv;bab"
        code_hash = hashlib.sha256(code_data.encode()).hexdigest()[:6]

        # 一時的に発行したコードを保存（生徒が後で確認できるようにする）
        # session['attendance_code'] = code_hash
        # session['code_timestamp'] = datetime.now().timestamp()  # 時刻も保存
        student_list=db.session.query(Student).filter_by(class_num = current_user.class_num).all()
        syusseki = [s.student_id for s in db.session.query(Syusseki).filter_by(year=year, month=month, day=day, periods=period).all()]


        return render_template("teacher_seiseki/display_code.html", code=code_hash, student_list=student_list, syusseki=syusseki)
        # else:
        #     flash("選択した授業は登録されていません。コードを発行できません。", "error")
        #     return redirect(url_for("teacher.seiseki.issue_code"))
    
    # 最初にTimetableから取得した授業一覧を表示する処理
    periods = [1, 2, 3]
    return render_template("teacher_seiseki/issue_code.html", periods=periods)

