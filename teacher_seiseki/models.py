from app import db

class Score(db.Model):
    __tablename__ = "score"
    score_id = db.Column(db.String, primary_key=True)
    class_num = db.Column(db.Integer)
    student_num = db.Column(db.Integer)
    subject_id = db.Column(db.String)
    subject_name = db.Column(db.String)
    attend_day = db.Column(db.Integer)

class Attend(db.Model):
    __tablename__ = "attend"