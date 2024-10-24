from datetime import datetime

from app import db


class Codes(db.Model):
    __tablename__ = "codes"
    id = db.Column(db.Integer, primary_key=True) # idをint型。主キーで設定
    code_name = db.Column(db.String)
    code_path = db.Column(db.String) # image_pathをString型で設定
    created_at = db.Column(db.DateTime, default=datetime.now) # created_atをDateTime型、初期値を現時刻で設定
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) # updated_atをDateTime型、初期値を現時刻、更新があった時刻を随時記録するよう設定