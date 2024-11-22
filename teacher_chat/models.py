from datetime import datetime
from app import db

class Chat(db.Model):
    __tablename__ = "chat"
    chat_id = db.Column(db.String, primary_key=True)
    teacher_num = db.Column(db.String)
    room_id = db.Column(db.String)
    discription = db.Column(db.String)
    chat_date = db.Column(db.DateTime, default=datetime.now)
    file_exist = db.Column(db.Boolean, default=1)

class Room(db.Model):
    __tablename__ = "room"
    room_id = db.Column(db.String, primary_key=True)
    room_name = db.Column(db.String)

class Room_Member(db.Model):
    __tablename__ = "room_member"
    room_member_id = db.Column(db.String, primary_key=True)
    room_id = db.Column(db.String)
    teacher_num = db.Column(db.String)

class Chat_Read(db.Model):
    __tablename__ = "chat_read"
    chat_id = db.Column(db.String, primary_key=True)
    room_member_id = db.Column(db.String, primary_key=True)
    read = db.Column(db.Boolean, default=0)

class Chat_File(db.Model):
    __tablename___ = "chat_file"
    file_id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String)

class File(db.Model):
    __tablename__ = "file"
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String)
    file_path = db.Column(db.String)
