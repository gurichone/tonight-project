from app import db  # Flaskアプリケーションとデータベースのインスタンスをインポート
from datetime import datetime

class Timetable(db.Model):
    __tablename__ = 'timetable'  # テーブル名を指定（任意）
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    month = db.Column(db.Integer)
    day = db.Column(db.Integer)
    weekday = db.Column(db.String(10))
    period1 = db.Column(db.String(100))
    period2 = db.Column(db.String(100))
    period3 = db.Column(db.String(100))
    notes = db.Column(db.String(200))
    event = db.Column(db.String(200))

    # この行を追加して、すでに定義されているテーブルを再定義できるようにする
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f"<Timetable {self.year}-{self.month}-{self.day}>"
