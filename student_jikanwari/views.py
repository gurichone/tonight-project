from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
import calendar
from app import db
from .models import Timetable
from teacher_jikanwari.models import SubjectDetails
from teacher_jikanwari.models import Timetable
from datetime import datetime
from auth.models import Subject, CourseSubject, ClassNum

# Blueprintの作成
jikanwari = Blueprint(
    "jikanwari",  # ブループリント名
    __name__,
    template_folder="templates",
    static_folder="static",
)

# 指定IDのエントリを取得する関数
def get_entry_by_id(entry_id):
    return Timetable.query.get(entry_id)

# 年と月を指定してデータを取得する関数
def get_entries_from_database(year, month):
    return Timetable.query.filter_by(year=year, month=month).all()

def get_entry_by_date(year, month, day):
    return Timetable.query.filter_by(year=year, month=month, day=day).first()

# 年と月を指定してJikanwariエントリを取得する関数
def get_jikanwari_entries(year, month):
    return Timetable.query.filter_by(year=year, month=month, class_num=current_user.class_num).all()

# 指定された年月の時間割を表示するルート
@jikanwari.route('/', methods=['GET'])
def s_jikanwari():
    now = datetime.now()
    selected_year = request.args.get('year', now.year, type=int)
    selected_month = request.args.get('month', now.month, type=int)

    # 年月を指定してJikanwariエントリを取得
    entries = get_jikanwari_entries(selected_year, selected_month)
    sbj_key_val = {subject.subject_id:subject.subject_name for subject in db.session.query(Subject).all()}
    # テンプレートに渡して時間割を表示
    return render_template('student_jikanwari/table.html', 
                           entries=entries,
                           selected_year=selected_year,
                           selected_month=selected_month,
                           sbj_key_val=sbj_key_val,
                           thisyear = now.year,)