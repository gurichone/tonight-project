from app import db

# このデータベースは変更する必要がある(2024/10/30現在)
# #をつけたカラムは他のデータベースを使用してhtmlに表示できるようにしたい

class Score(db.Model):
    __tablename__ = "score"
    score_id = db.Column(db.Integer, primary_key=True)
    class_num = db.Column(db.String)
    id = db.Column(db.String)
    subject_id = db.Column(db.String(10))
    assessment_id = db.Column(db.String(1))
    attend_day = db.Column(db.Integer)
# attend_dayは出席日数を表すカラムだが、出席に数はSyussekiテーブルにcount文を使うことで取得できるため実質使わないことにする
# ただし消したらエラーが怖いから放置

class Syusseki(db.Model):
    __tablename__ = "syusseki"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    periods = db.Column(db.Integer)