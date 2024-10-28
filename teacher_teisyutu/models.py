from app import db

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.String, primary_key=True)
    subject_id = db.Column(db.String(10), nullable=False)
    subject_name = db.Column(db.String(20), nullable=False)
    course_name = db.Column(db.String(30))

class Course(db.Model):
    __tablename__ = "course"
    class_num = db.Column(db.String(4), primary_key=True)
    course_name = db.Column(db.String(30), nullable=False)

class Submission(db.Model):
    __tablename__ = "submission"
    submission_id = db.Column(db.String, primary_key=True)
    submission_name = db.Column(db.String, nullable=False)
    subject_id = db.Column(db.String, db.ForeignKey('subject.subject_id'), nullable=False)
    course_name = db.Column(db.String, db.ForeignKey('course.course_name'), nullable=False)
    submission_type = db.Column(db.String, nullable=False)
    submissin_rimit = db.Column(db.DateTime, nullable=False)
    scoreing_type = db.Column(db.Integer, nullable=False)
    question_file = db.Column(db.String)
    testcase_file = db.Column(db.String)

class SubmissionSituation(db.Model):
    __tablename__ = "submission_situation"
    submission_id = db.Column(db.String, db.ForeignKey('submission.submission_id'), primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey('student.id'), nullable=False)
    point = db.Column(db.Integer)
    submitted = db.Column(db.Boolean, nullable=False, default=0)
    file = db.Column(db.String)