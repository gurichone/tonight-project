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
    timetable_data = Timetable.query.order_by(
        Timetable.year, 
        Timetable.month, 
        Timetable.day
    ).all()
    return render_template('teacher_jikanwari/table.html', data=timetable_data)

# エントリ追加ルート
@jikanwari.route('/add', methods=['POST'])
def add_entry():
    new_entry = Timetable(
        year=int(request.form['year']),
        month=int(request.form['month']),
        day=int(request.form['day']),
        weekday=request.form['weekday'],
        period1=request.form['period1'],
        period2=request.form['period2'],
        period3=request.form['period3'],
        notes=request.form['notes'],
        event=request.form['event']
    )
    db.session.add(new_entry)
    db.session.commit()
    
    return redirect(url_for('teacher.jikanwari.t_jikanwari'))  # 修正

@jikanwari.route('/add', methods=['GET'])
def show_add_entry():
    return render_template('teacher_jikanwari/add_entry.html')

# エントリ編集ルート
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
        
        return redirect(url_for('teacher.jikanwari.t_jikanwari'))  
    return render_template('teacher_jikanwari/edit_entry.html', entry=entry)

# エントリ削除確認ルート
@jikanwari.route('/delete_confirmation/<int:id>', methods=['GET'])
def delete_confirmation(id):
    entry = get_entry_by_id(id)
    if entry:
        return render_template('teacher_jikanwari/delete_confirmation.html', entry=entry)
    else:
        
        return redirect(url_for('teacher.jikanwari.t_jikanwari'))  # 修正

# エントリ削除ルート
@jikanwari.route('/delete/<int:id>', methods=['POST'])
def delete_entry(id):
    # 指定されたIDのエントリーを取得
    entry = Timetable.query.get(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()
    return redirect(url_for('teacher.jikanwari.t_jikanwari')) 




