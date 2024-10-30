from app import db

# このデータベースは変更する必要がある(2024/10/30現在)
class Score(db.Model):
    __tablename__ = "score"
    score_id = db.Column(db.Integer, primary_key=True)
    class_num = db.Column(db.String)
    student_num = db.Column(db.String)#
    student_name = db.Column(db.String)
    subject_id = db.Column(db.String(10))
    subject_name = db.Column(db.String)
    assessment_id = db.Column(db.String(1))#
    attend_day = db.Column(db.Integer)