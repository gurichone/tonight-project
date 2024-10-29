from app import db

class Score(db.Model):
    __tablename__ = "score"
    score_id = db.Column(db.String, primary_key=True)
    class_num = db.Column(db.Integer)
    student_num = db.Column(db.Integer)
    student_name = db.Column(db.String(20))
    subject_id = db.Column(db.String(10))
    subject_name = db.Column(db.String(20))
    assessment_id = db.Column(db.String(1))
    attend_day = db.Column(db.Integer)