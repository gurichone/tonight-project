from flask import Blueprint, render_template, request, redirect, url_for  # requestをインポート
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
    {"day": "Monday", "period1": "Math", "period2": "Science", "period3": "History", "notes": "Bring calculator", "event": "Quiz"},
    {"day": "Tuesday", "period1": "English", "period2": "PE", "period3": "Art", "notes": "Bring sports kit", "event": ""},
    # 必要に応じてデータを追加
]

# ルートの定義
@jikanwari.route('/')
def t_jikanwari():
    timetable_data = Timetable.query.all()  # データベースから全エントリを取得
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
        "day": request.form['day'],
        "period1": request.form['period1'],
        "period2": request.form['period2'],
        "period3": request.form['period3'],
        "notes": request.form['notes'],
        "event": request.form['event']
    }
    timetable_data.append(new_entry)  # 新しい項目を追加
    return redirect(url_for('teacher.jikanwari.t_jikanwari'))  # 修正: 正しいエンドポイントにリダイレクト

@jikanwari.route('/add', methods=['GET'])
def show_add_entry():
    return render_template('teacher_jikanwari/add_entry.html')



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)