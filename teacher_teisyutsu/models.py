from app import db

class Subject(db.Model):
    __tablename__ = "subject"
    subject_id = db.Column(db.String, primary_key=True)
    subject_name = db.Column(db.String)
    course_name = db.Column(db.String, primary_key=True)

class Course(db.Model):
    __tablename__ = "course"
    class_num = db.Column(db.String, primary_key=True)
    course_name = db.Column(db.String)

class Submission(db.Model):
    __tablename__ = "submission"
    submission_id = db.Column(db.String, primary_key=True)
    submission_name = db.Column(db.String)
    subject_id = db.Column(db.String)
    course_name = db.Column(db.String)
    submission_type = db.Column(db.String)
    submissin_rimit = db.Column(db.DateTime)
    scoreing_type = db.Column(db.Integer)
    question_file = db.Column(db.String)
    testcase_file = db.Column(db.String)

class SubmissionSituation(db.Model):
    __tablename__ = "submission_situation"
    submission_id = db.Column(db.String, primary_key=True)
    student_id = db.Column(db.String)
    point = db.Column(db.Integer)
    submitted = db.Column(db.Boolean, default=0)
    file = db.Column(db.String)
