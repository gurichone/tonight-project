from app import db

class Timetable(db.Model):
    __tablename__ = "timetable"
    id = db.Column(db.Integer, primary_key=True)
    class_num = db.Column(db.String)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    weekday = db.Column(db.String(10), nullable=False)
    period1 = db.Column(db.Integer)
    period2 = db.Column(db.Integer)
    period3 = db.Column(db.Integer)
    notes = db.Column(db.String(200))
    event = db.Column(db.String(100))


class SubjectDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, nullable=False)
    class_num = db.Column(db.String)
    periods = db.Column(db.Integer, nullable=False)
    units = db.Column(db.Integer, nullable=False, default=1)

