from flask import Blueprint, render_template, redirect, url_for, request
from auth.models import Student
from teacher_student.forms import StudentSearch
from app import db

student = Blueprint(
    "student",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@student.route("/")
def teacher_student():
    return render_template("teacher_student/list_menu.html")

@student.route("/student_list", methods=["GET", "POST"])
def student_list():
    # フォームインスタンスの作成
    stu_list = StudentSearch()
    
    # 学生リストの取得
    students = Student.query.with_entities(
        Student.id,
        Student.class_num,
        Student.student_name
    ).all()

    # クラス番号と学生IDの選択肢を設定（プレースホルダーを追加）
    clases = set((s.class_num) for s in students)
    stu_list.class_num.choices = [("", "ーー")] + [(s, s) for s in clases]
    
    ids = ((s.id) for s in students)
    stu_list.id.choices = [("", "ーー")] + [(s, s) for s in ids]

    # 検索条件に基づいてクエリをフィルタリング
    query = Student.query

    if stu_list.validate_on_submit():
        # student_idが選択されていればフィルタリング
        if stu_list.id.data:
            query = query.filter(Student.id == stu_list.id.data)
        
        # class_numが選択されていればフィルタリング
        if stu_list.class_num.data:
            query = query.filter(Student.class_num == stu_list.class_num.data)

        # student_nameが入力されていればフィルタリング
        if stu_list.student_name.data:
            query = query.filter(Student.student_name.like(f"%{stu_list.student_name.data}%"))

    # フィルタリング結果を取得
    students = query.with_entities(
        Student.id,
        Student.class_num,
        Student.student_name
    ).all()

    # メッセージ設定
    if not students:
        message = "検索条件に合う学生は見つかりませんでした"
    else:
        message = f"{len(students)}件の学生が見つかりました"

    return render_template(
        'teacher_student/student_list.html', 
        stu_list=stu_list, 
        students=students, 
        message=message
    )
