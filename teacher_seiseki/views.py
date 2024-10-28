from flask import Blueprint, render_template, redirect, url_for, request
from app import db
from teacher_seiseki.forms import SearchScore
from teacher_seiseki.models import Score

seiseki = Blueprint(
    "seiseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 成績画面は三つの要素から絞り込みをして検索する
@seiseki.route("/")
def search():
    # db.session.query(Score).all()
        
    return render_template("/teacher_seiseki/index.html")

@seiseki.route("/add", methods=["GET"])
def add():
    return None

@seiseki.route("/attendance")
def attendance():
    return None