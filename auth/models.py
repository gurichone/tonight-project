from datetime import datetime

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# teacherテーブル
class Teacher(db.Model, UserMixin):
    __tablename__ = "teacher"
    id = db.Column(db.String, primary_key=True)
    teacher_name = db.Column(db.String, index=True)
    teacher_email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    class_num = db.Column(db.String)
    icon_path = db.Column(db.String)
    authority = db.Column(db.Boolean)

    @property
    def password(self):
        raise AttributeError("読み込み不可")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_duplicate_email(self):
        return Teacher.query.filter_by(teacher_email=self.teacher_email).first() is not None or Student.query.filter_by(student_email=self.teacher_email).first() is not None

@login_manager.user_loader
def load_user(id):
    if len(id) == 6:
        return Teacher.query.get(id)
    else:
        return Student.query.get(id)

# studentテーブル
class Student(db.Model, UserMixin):
    __tablename__ = "student"
    id = db.Column(db.String, primary_key=True)
    student_name = db.Column(db.String, index=True)
    student_email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    entrollment_year = db.Column(db.Integer)
    birth_date = db.Column(db.Date)
    school_id = db.Column(db.String)
    course_id = db.Column(db.String)
    class_num = db.Column(db.String)
    icon_path = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError("読み込み不可")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_duplicate_email(self):
        return Student.query.filter_by(student_email=self.student_email).first() is not None or Teacher.query.filter_by(teacher_email=self.student_email).first() is not None

# @login_manager.user_loader
# def load_student(student_id):
#     return Student.query.get(student_id)


class Subject(db.Model):
    __tablename__ = "subject"
    subject_id = db.Column(db.Integer, primary_key=True)
    subject_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = "course"
    course_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    course_name = db.Column(db.String)

class ClassNum(db.Model):
    __tablename__ = "class_num"
    class_num = db.Column(db.String, primary_key=True)
    course_id = db.Column(db.Integer)

class CourseSubject(db.Model):
    __tablename__ = "course_subject"
    course_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, primary_key=True)

class School(db.Model):
    __tablename__ = "school"
    school_id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String)