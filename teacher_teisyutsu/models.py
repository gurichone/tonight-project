from app import db

class Submission(db.Model):
    __tablename__ = "submission"
    submission_id = db.Column(db.Integer, primary_key=True)
    submission_name = db.Column(db.String)
    subject_id = db.Column(db.Integer)
    class_num = db.Column(db.String)
    submission_type = db.Column(db.Integer)
    submission_rimit = db.Column(db.DateTime)
    scoring_type = db.Column(db.Integer)
    question = db.Column(db.String)
    testcase = db.Column(db.String)

class Personal_Submission(db.Model):
    __tablename__ = "personal_submission"
    submission_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, primary_key=True)
    point = db.Column(db.Integer)
    submitted = db.Column(db.Boolean, default=0)
    file = db.Column(db.String)
