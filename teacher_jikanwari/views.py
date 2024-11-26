from flask import Blueprint, render_template, request, redirect, url_for, flash
import calendar
import sqlite3
from calendar import monthrange, weekday
from app import db
from .models import Timetable
from teacher_jikanwari.models import SubjectDetails
from teacher_jikanwari.models import Timetable

# Blueprintの作成
jikanwari = Blueprint(
    "jikanwari",  # ブループリント名
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 指定IDのエントリを取得する関数
def get_entry_by_id(entry_id):
    return Timetable.query.get(entry_id)

# 年と月を指定してデータを取得する関数
def get_entries_from_database(year, month):
    return Timetable.query.filter_by(year=year, month=month).all()

def get_entry_by_date(year, month, day):
    return Timetable.query.filter_by(year=year, month=month, day=day).first()

# 年と月を指定してJikanwariエントリを取得する関数
def get_jikanwari_entries(year, month):
    return Timetable.query.filter_by(year=year, month=month).all()

def get_subjects():
    connection = sqlite3.connect('local.sqlite')
    cursor = connection.cursor()
    cursor.execute("SELECT subject_name FROM subject")  # subject_nameが科目名を格納していると仮定
    subjects = cursor.fetchall()
    connection.close()
    return [subject[0] for subject in subjects]

# 指定された年月の時間割を表示するルート
@jikanwari.route('/', methods=['GET'])
def t_jikanwari():
    selected_year = request.args.get('year', 2024, type=int)
    selected_month = request.args.get('month', 1, type=int)

    # 年月を指定してJikanwariエントリを取得
    entries = get_jikanwari_entries(selected_year, selected_month)

    # テンプレートに渡して時間割を表示
    return render_template('teacher_jikanwari/table.html', 
                           entries=entries,
                           selected_year=selected_year,
                           selected_month=selected_month)

@jikanwari.route('/add_entry', methods=['GET', 'POST'])
def add_entry():

    subjects = get_subjects()

    selected_year = request.args.get('year', default=2024, type=int)
    selected_month = request.args.get('month', default=1, type=int)

    # 月の日数を取得
    number_of_days = calendar.monthrange(selected_year, selected_month)[1]

    # 曜日のリスト
    weekdays = ['月', '火', '水', '木', '金', '土', '日']

    # 日付と曜日の組み合わせ
    dates_and_weekdays = []
    for day in range(1, number_of_days + 1):
        weekday = calendar.weekday(selected_year, selected_month, day)  # 0 = 月曜, 6 = 日曜
        dates_and_weekdays.append({
            'day': day,
            'weekday': weekdays[weekday]
        })

    # 選択された年と月のデータを取得
    existing_entries = Timetable.query.filter_by(year=selected_year, month=selected_month).all()
    existing_data = {entry.day: entry for entry in existing_entries}

    if request.method == 'POST':
        # POSTリクエストが送られた場合、新しいエントリを追加
        for day in range(1, number_of_days + 1):
            period1 = request.form.get(f'period1_{day}')
            period2 = request.form.get(f'period2_{day}')
            period3 = request.form.get(f'period3_{day}')
            notes = request.form.get(f'notes_{day}')
            event = request.form.get(f'event_{day}')

            # 既存のエントリをチェック
            existing_entry = Timetable.query.filter_by(year=selected_year, month=selected_month, day=day).first()

            weekday = calendar.weekday(selected_year, selected_month, day)
            weekday_name = weekdays[weekday]

            if existing_entry:
                # 既存のエントリを更新
                existing_entry.period1 = period1
                existing_entry.period2 = period2
                existing_entry.period3 = period3
                existing_entry.notes = notes
                existing_entry.event = event
            else:
                # 新しいエントリを作成
                new_entry = Timetable(
                    year=selected_year,
                    month=selected_month,
                    day=day,
                    weekday=weekday_name,
                    period1=period1,
                    period2=period2,
                    period3=period3,
                    notes=notes,
                    event=event
                )
                db.session.add(new_entry)  # 新しいエントリを追加
                db.session.commit()  # 一度だけコミットしてデータベースに保存

        # データ追加後は時間割のページにリダイレクト
        return redirect(url_for('teacher.jikanwari.t_jikanwari'))

    # GETリクエストの場合はフォームを表示
    return render_template('teacher_jikanwari/add_entry.html', 
                           subjects=subjects,
                           selected_year=selected_year,
                           selected_month=selected_month, 
                           dates_and_weekdays=dates_and_weekdays,
                           existing_data=existing_data)




@jikanwari.route('/save_timetable', methods=['POST'])
def save_timetable():
    # フォームデータを取得
    form = dict(request.form)

    # フォームデータを確認（コンソールに出力）
    print(form)  # フォームデータの内容を確認

    selected_year = int(form['year'])
    selected_month = int(form['month'])

    # 年月に基づいてデータを取得
    dates_and_weekdays = Timetable.query.filter_by(year=selected_year, month=selected_month).all()
    if dates_and_weekdays:
        for date in dates_and_weekdays:
            period1 = form["period1_"+str(date.day)]
            period2 = form["period2_"+str(date.day)]
            period3 = form["period3_"+str(date.day)]
            notes = form["notes_"+str(date.day)]
            event = form["event_"+str(date.day)]

            entry = Timetable.query.filter_by(day=date.day, month=selected_month, year=selected_year).first()
            
            # 既存のエントリを更新
            entry.period1 = period1
            entry.period2 = period2
            entry.period3 = period3
            entry.notes = notes
            entry.event = event
            
            db.session.add(entry)
            db.session.commit()  # すべての変更を保存
    else:
        # その月の日数を取得
        days_in_month = monthrange(selected_year, selected_month)[1]
        weekdays = ['月', '火', '水', '木', '金', '土', '日']

        for day in range(1, days_in_month + 1):  # 1日からスタート
            period1 = form["period1_"+str(day)]
            period2 = form["period2_"+str(day)]
            period3 = form["period3_"+str(day)]
            notes = form["notes_"+str(day)]
            event = form["event_"+str(day)]
            
            # 新しいエントリを作成
            entry = Timetable(
                year=selected_year,
                month=selected_month,
                day=day,
                weekday=weekdays[weekday(selected_year, selected_month, day)],  # 曜日を計算
                period1=period1,
                period2=period2,
                period3=period3,
                notes=notes,
                event=event
            )
            db.session.add(entry)
            db.session.commit()

    # 時間割にリダイレクト
    return redirect(url_for("teacher.jikanwari.t_jikanwari"))

# クラス一覧表示
@jikanwari.route('/class_list')
def class_list():
    subjects = SubjectDetails.query.all()  # データベースから授業のデータを取得
    return render_template('teacher_jikanwari/class_list.html', subjects=subjects)


# クラス数の表示
@jikanwari.route('/show_class_count', methods=['GET', 'POST'])
def show_class_count():
    error_message = None

    if request.method == 'POST':
        subject_name = request.form['subject_name']
        periods = int(request.form['periods'])

        # 既存の科目名があるかチェック
        existing_subject = SubjectDetails.query.filter_by(name=subject_name).first()

        if existing_subject:
            error_message = "この科目名は登録済みです"
        elif periods <= 15:
            error_message = "コマ数は15コマ以上でなければなりません。"
        else:
            # 新しい科目をデータベースに追加
            new_subject = SubjectDetails(name=subject_name, periods=periods)
            db.session.add(new_subject)
            db.session.commit()

            return redirect(url_for('jikanwari.class_list'))

    return render_template('teacher_jikanwari/show_class_count.html', error_message=error_message)

# クラス削除確認画面
@jikanwari.route('/class/delete_count/<int:subject_id>', methods=['GET', 'POST'])
def delete_class_count(subject_id):
    subject = SubjectDetails.query.get(subject_id)
    if request.method == 'POST':
        db.session.delete(subject)
        db.session.commit()
        return redirect(url_for('jikanwari.class_list'))

    return render_template('teacher_jikanwari/delete_class_count.html', subject=subject)

# 編集画面の表示
# 編集画面の表示 (新たに追加)
@jikanwari.route('/edit_class_count/<int:subject_id>', methods=['GET', 'POST'])
def edit_class_count(subject_id):
    subject = SubjectDetails.query.get(subject_id)

    if request.method == 'POST':
        subject.name = request.form['name']
        subject.periods = request.form['periods']
        
        db.session.commit()
        return redirect(url_for('jikanwari.class_list'))

    return render_template('teacher_jikanwari/edit_class_count.html', subject=subject)

