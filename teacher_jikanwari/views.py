from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from .models import Timetable
from teacher_jikanwari.models import SubjectDetails

# Blueprintの作成
jikanwari = Blueprint(
    "jikanwari",  # ブループリント名
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 指定IDのエントリを取得する関数
def get_entry_by_id(id):
    return Timetable.query.get(id)

# タイムテーブルの表示ルート
@jikanwari.route('/')
def t_jikanwari():
    timetable_data = Timetable.query.with_entities(
        Timetable.id,          
        Timetable.year,
        Timetable.month,
        Timetable.day,
        Timetable.weekday,
        Timetable.period1,
        Timetable.period2,
        Timetable.period3,
        Timetable.notes,
        Timetable.event
    ).order_by(Timetable.year, Timetable.month, Timetable.day).all()
    return render_template('teacher_jikanwari/table.html', data=timetable_data)

# エントリ追加ルート（POSTメソッド）
@jikanwari.route('/teacher/jikanwari/add_entry', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        year = int(request.form['year'])
        month = int(request.form['month'])
        day = int(request.form['day'])
        weekday = request.form['weekday']

        # 同じ日付のエントリが存在するか確認
        existing_entry = Timetable.query.filter_by(year=year, month=month, day=day, weekday=weekday).first()

        if existing_entry:
            error_message = "この日付のエントリは既に存在します。別の日付を選択してください。"
            return render_template('teacher_jikanwari/add_entry.html', error=error_message)

        new_entry = Timetable(
            year=year,
            month=month,
            day=day,
            weekday=weekday,
            period1=request.form['period1'],
            period2=request.form['period2'],
            period3=request.form['period3'],
            notes=request.form['notes'],
            event=request.form['event']
        )
        db.session.add(new_entry)
        db.session.commit()

        # 追加後、一覧画面にリダイレクト
        return redirect(url_for('teacher.jikanwari.t_jikanwari'))


    return render_template('teacher_jikanwari/add_entry.html')

# エントリ編集ルート（GET/POSTメソッド）
@jikanwari.route('/teacher/jikanwari/edit_entry/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = get_entry_by_id(id)
    if not entry:
        return redirect(url_for('jikanwari.t_jikanwari'))  # 正しいエンドポイント名を使用

    if request.method == 'POST':
        entry.year = int(request.form['year'])
        entry.month = int(request.form['month'])
        entry.day = int(request.form['day'])
        entry.weekday = request.form['weekday']
        entry.period1 = request.form['period1']
        entry.period2 = request.form['period2']
        entry.period3 = request.form['period3']
        entry.notes = request.form['notes']
        entry.event = request.form['event']

        db.session.commit()

        # 更新後、一覧画面にリダイレクト
        return redirect(url_for('jikanwari.t_jikanwari'))  # 正しいエンドポイント名を使用

    return render_template('teacher_jikanwari/edit_entry.html', entry=entry)

# エントリ削除確認ルート
@jikanwari.route('/delete_confirmation/<int:id>', methods=['GET'])
def delete_confirmation(id):
    entry = get_entry_by_id(id)
    if entry:
        return render_template('teacher_jikanwari/delete_confirmation.html', entry=entry)
    else:
        return redirect(url_for('jikanwari.t_jikanwari'))  # 正しいエンドポイント名を使用

# エントリ削除ルート
@jikanwari.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    entry = Timetable.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()

    # 削除後、一覧画面にリダイレクト
    return redirect(url_for('jikanwari.t_jikanwari'))  # 正しいエンドポイント名を使用

# クラス一覧表示
@jikanwari.route('/class_list')
def class_list():
    subjects = SubjectDetails.query.all()
    return render_template('teacher_jikanwari/class_list.html', subjects=subjects)

# クラス数の表示
@jikanwari.route('/show_class_count', methods=['GET', 'POST'])
def show_class_count():
    error_message = None  # エラーメッセージを格納する変数

    if request.method == 'POST':
        subject_name = request.form['subject_name']
        periods = int(request.form['periods'])

        # 既に同じ名前の科目が存在するかチェック
        existing_subject = SubjectDetails.query.filter_by(name=subject_name).first()

        if existing_subject:
            error_message = "この科目名は登録済みです"
        elif periods <= 15:
            error_message = "コマ数は15コマ以上でなければなりません。"
        else:
            # コマ数が15コマ以上で、かつ同じ科目名がない場合、データベースに新しい授業情報を保存
            new_subject = SubjectDetails(name=subject_name, periods=periods)
            db.session.add(new_subject)
            db.session.commit()

            # 登録後に授業数一覧画面へリダイレクト
            return redirect(url_for('teacher.jikanwari.class_list'))

    return render_template('teacher_jikanwari/show_class_count.html', error_message=error_message)


# クラス削除確認画面
@jikanwari.route('/class/delete_count/<int:subject_id>', methods=['GET', 'POST'])
def delete_class_count(subject_id):
    subject = SubjectDetails.query.get(subject_id)
    if request.method == 'POST':
        # 削除処理
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for('teacher.jikanwari.class_list'))  # 削除後にクラス一覧ページにリダイレクト

    # GETリクエストの場合、削除確認画面を表示
    return render_template('teacher_jikanwari/delete_class_count.html', subject=subject)

# 編集画面の表示
@jikanwari.route('/class/edit/<int:subject_id>', methods=['GET', 'POST'])
def edit_class_count(subject_id):
    subject = SubjectDetails.query.get(subject_id)

    if request.method == 'POST':
        # フォームからデータを取得
        subject.name = request.form['name']
        subject.periods = request.form['periods']
        
        # データベースを更新
        db.session.commit()
        return redirect(url_for('teacher.jikanwari.class_list'))  # 編集後、授業数一覧にリダイレクト

    return render_template('teacher_jikanwari/edit_class_count.html', subject=subject)