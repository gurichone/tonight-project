from flask import Blueprint, render_template, request, redirect, url_for,flash
from app import db
from .models import Timetable

# Blueprintの作成
jikanwari = Blueprint(
    "jikanwari",
    __name__,
    template_folder="templates",
    static_folder="static",
)

def get_entry_by_id(id):
    """指定されたIDのエントリをデータベースから取得する関数"""
    return Timetable.query.get(id)

def delete_entry_by_id(id):
    """指定されたIDのエントリをデータベースから削除する関数"""
    entry = get_entry_by_id(id)
    if entry:
        db.session.delete(entry)
        db.session.commit()  # 変更をコミット

# タイムテーブルデータのサンプル
timetable_data = [
    {"year": 2024, "month": 10, "day": 28, "weekday": "月曜日", "period1": "Math", "period2": "Science", "period3": "History", "notes": "Bring calculator", "event": "Quiz"},
    {"year": 2024, "month": 10, "day": 29, "weekday": "火曜日", "period1": "English", "period2": "PE", "period3": "Art", "notes": "Bring sports kit", "event": ""},
    # 必要に応じてデータを追加
]

# ルートの定義
@jikanwari.route('/')
def t_jikanwari():
    timetable_data = Timetable.query.all()  # データベースから全てのデータを取得
    return render_template('teacher_jikanwari/table.html', data=timetable_data)


# Flaskアプリケーションの作成
def create_app():
    app = Flask(__name__)

    # Blueprintの登録
    app.register_blueprint(jikanwari, url_prefix='/teacher')

    return app

@jikanwari.route('/add', methods=['POST'])
def add_entry():
    # フォームからデータを取得
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
    # データベースに保存
    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for('teacher.jikanwari.t_jikanwari'))


@jikanwari.route('/add', methods=['GET'])
def show_add_entry():
    return render_template('teacher_jikanwari/add_entry.html')

@jikanwari.route('/teacher/jikanwari/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    entry = Timetable.query.get_or_404(id)
    if request.method == 'POST':
        # 更新データの取得
        entry.year = request.form['year']
        entry.month = request.form['month']
        entry.day = request.form['day']
        entry.period1 = request.form['period1']
        entry.period2 = request.form['period2']
        entry.period3 = request.form['period3']
        entry.notes = request.form['notes']
        entry.event = request.form['event']

        # データベースに保存
        db.session.commit()
        flash("時間割が更新されました")
        return redirect(url_for('teacher.jikanwari.t_jikanwari'))

    # GETリクエストの場合、編集画面を表示
    return render_template('teacher_jikanwari/edit_entry.html', entry=entry)



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
