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