from app import db

class Information(db.Model):
    __tablename__ = "information"
    info_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    discription = db.Column(db.String)
    teacher_num = db.Column(db.String)


class Get_Information(db.Model):
    __tablename__ = "get_information"
    info_id = db.Column(db.Integer, primary_key=True)
    student_num = db.Column(db.String, primary_key=True)
    read = db.Column(db.Boolean, default=0)