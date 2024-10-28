from flask import Blueprint, render_template, request, redirect, url_for
from app import db

# Blueprintの作成
jikanwari = Blueprint(
    "jikanwari",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# タイムテーブルデータのサンプル
timetable_data = [
    {"year": 2024, "month": 10, "day": 28, "weekday": "月曜日", "period1": "Math", "period2": "Science", "period3": "History", "notes": "Bring calculator", "event": "Quiz"},
    {"year": 2024, "month": 10, "day": 29, "weekday": "火曜日", "period1": "English", "period2": "PE", "period3": "Art", "notes": "Bring sports kit", "event": ""},
    # 必要に応じてデータを追加
]

# ルートの定義
@jikanwari.route('/')
def t_jikanwari():
    return render_template('teacher_jikanwari/table.html', data=timetable_data)

# Flaskアプリケーションの作成
def create_app():
    app = Flask(__name__)

    # Blueprintの登録
    app.register_blueprint(jikanwari, url_prefix='/teacher')

    return app

@jikanwari.route('/add', methods=['POST'])
def add_entry():
    new_entry = {
        "year": request.form['year'],  # 西暦
        "month": request.form['month'],  # 月
        "day": request.form['day'],  # 日
        "weekday": request.form['weekday'],  # 曜日
        "period1": request.form['period1'],  # 1時間目
        "period2": request.form['period2'],  # 2時間目
        "period3": request.form['period3'],  # 3時間目
        "notes": request.form['notes'],  # 備考
        "event": request.form['event']  # イベント
    }
    timetable_data.append(new_entry)  # 新しい項目を追加
    return redirect(url_for('teacher.jikanwari.t_jikanwari')) 

@jikanwari.route('/add', methods=['GET'])
def show_add_entry():
    return render_template('teacher_jikanwari/add_entry.html')

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
