from app import db

class Timetable(db.Model):
    __tablename__ = "timetable"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    weekday = db.Column(db.String(10), nullable=False)
    period1 = db.Column(db.String(50))
    period2 = db.Column(db.String(50))
    period3 = db.Column(db.String(50))
    notes = db.Column(db.String(200))
    event = db.Column(db.String(100))


class SubjectDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    periods = db.Column(db.Integer, nullable=False)

