from flask import Blueprint, render_template, request, redirect, url_for
from app import db
from .models import Timetable

# Blueprintの作成
jikanwari = Blueprint(
    "jikanwari",
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
    # 日付の早い順にエントリを取得
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
    ).order_by(Timetable.year, Timetable.month, Timetable.day).all()  # ここを追加
    return render_template('teacher_jikanwari/table.html', data=timetable_data)


# エントリ追加ルート（GETメソッド）
@jikanwari.route('/add', methods=['GET'])
def show_add_entry():
    return render_template('teacher_jikanwari/add_entry.html')

# エントリ追加ルート（POSTメソッド）
@jikanwari.route('/add', methods=['POST'])
def add_entry():
    year = int(request.form['year'])
    month = int(request.form['month'])
    day = int(request.form['day'])
    weekday = request.form['weekday']

    # 同じ日付のエントリが存在するか確認
    existing_entry = Timetable.query.filter_by(year=year, month=month, day=day, weekday=weekday).first()

    if existing_entry:
        # エントリが既に存在する場合、エラーメッセージを表示
        error_message = "この日付のエントリは既に存在します。別の日付を選択してください。"
        return render_template('teacher_jikanwari/add_entry.html', error=error_message)

    # 新しいエントリを作成
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
    
    return redirect(url_for('teacher.jikanwari.t_jikanwari'))  # 修正されたエンドポイント名


@jikanwari.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = Timetable.query.get_or_404(id)
    if request.method == 'POST':
        entry.year = request.form['year']
        entry.month = request.form['month']
        entry.day = request.form['day']
        entry.period1 = request.form['period1']
        entry.period2 = request.form['period2']
        entry.period3 = request.form['period3']
        entry.notes = request.form['notes']
        entry.event = request.form['event']
        db.session.commit()
        
        return redirect(url_for('teacher.jikanwari.t_jikanwari'))  # エンドポイントを修正
    # GETリクエストの場合、編集ページをレンダリング
    return render_template('teacher_jikanwari/edit_entry.html', entry=entry)


# エントリ削除確認ルート
@jikanwari.route('/delete_confirmation/<int:id>', methods=['GET'])
def delete_confirmation(id):
    entry = get_entry_by_id(id)
    if entry:
        return render_template('teacher_jikanwari/delete_confirmation.html', entry=entry)
    else:
        return redirect(url_for('jikanwari.t_jikanwari'))  # 修正されたエンドポイント名

# エントリ削除ルート
@jikanwari.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    entry = Timetable.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('teacher.jikanwari.t_jikanwari'))  # 修正されたエンドポイント名

# 授業数登録ページ
@jikanwari.route('/lesson_count')
def lesson_count():
    # 授業数を取得
    lesson_count = Timetable.query.count()
    return render_template('teacher_jikanwari/lesson_count.html', lesson_count=lesson_count)
