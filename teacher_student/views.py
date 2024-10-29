from flask import Blueprint, render_template, redirect, url_for, request
from auth.models import Student
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

@student.route("/student_list", methods=['GET'])
def student_list():
    # GETパラメータを取得
    id_query = request.args.get('id')
    student_name_query = request.args.get('student_name')
    class_num_query = request.args.get('class_num')

    # クラス番号と生徒番号の選択肢を取得(重複しないようにdistinctを使用)
    student_ids = [student.id for student in Student.query.with_entities(Student.id).distinct().all()]
    class_nums = [student.class_num for student in Student.query.with_entities(Student.class_num).distinct().all()]

    # クエリの構築
    query = Student.query
    if id_query and id_query != "--": # --が選択されている場合は未入力とする
        query = query.filter(Student.id == id_query)
    if student_name_query:
        query = query.filter(Student.student_name.like(f"%{student_name_query}%"))
    if class_num_query and class_num_query != "--": # --が選択されている場合は未入力とする
        query = query.filter(Student.class_num == class_num_query)

    # 最終的なクエリの実行
    students = query.with_entities(Student.id, Student.student_name, Student.class_num).all()

    return render_template('teacher_student/student_list.html',
                           students = students,
                           student_ids = student_ids,
                           class_nums = class_nums,
                           id_query = id_query,
                           student_name_query = student_name_query,
                           class_num_query = class_num_query)

    # students = db.session.query(Student).with_entities(Student.id, Student.student_name, Student.class_num).all()
    # return render_template('teacher_student/student_list.html', students = students)