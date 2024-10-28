from app import db

class Timetable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(50), nullable=False)
    period1 = db.Column(db.String(50), nullable=False)
    period2 = db.Column(db.String(50), nullable=False)
    period3 = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(200), nullable=True)
    event = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<Timetable {self.day}>'
