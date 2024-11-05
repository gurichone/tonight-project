from flask import Blueprint, render_template, redirect, url_for, request, session
from auth.models import Student,Teacher, School, Course
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
    
    # 生徒リストの取得
    students = Student.query.with_entities(
        Student.id,
        Student.class_num,
        Student.student_name
    ).all()

    # クラス番号と生徒番号の選択肢を設定（プレースホルダーを追加）
    clases = set((s.class_num) for s in students)
    stu_list.class_num.choices = [("", "--")] + [(s, s) for s in clases]
    
    ids = ((s.id) for s in students)
    stu_list.id.choices = [("", "--")] + [(s, s) for s in ids]

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

        # 検索条件をフォームに設定
    stu_list.id.data = request.form.get('id', "")  # 生徒番号
    stu_list.class_num.data = request.form.get('class_num', "")  # クラス番号
    stu_list.student_name.data = request.form.get('student_name', "")  # 氏名

    # メッセージ設定
    if not students:
        message = "検索条件に合う生徒は見つかりませんでした"
    else:
        message = f"{len(students)}件の生徒が見つかりました"


    # print("\n\n\n", stu_list.class_num.data, type(stu_list.class_num.data), "\n", stu_list.class_num.choices, "\n\n\n")
    # print("\n\n\n", stu_list.id.data, type(stu_list.id.data), "\n", stu_list.id.choices, "\n\n\n")

    return render_template(
        'teacher_student/student_list.html', 
        stu_list=stu_list, 
        students=students, 
        message=message
    )

@student.route("/student/<string:id>")
def student_detail(id):
    # Studentクラスの全フィールドを取得
    student = Student.query.filter_by(id=id).first_or_404()
    
    # 学校名とコース名を取得
    school = School.query.filter_by(school_id=student.school_id).first()
    course = Course.query.filter_by(course_id=student.course_id).first()

    return render_template(
        'teacher_student/student_detail.html',
        student=student,
        school_name=school.school_name if school else "不明",
        course_name=course.course_name if course else "不明"
    )

@student.route("/class_list")
def class_list():
    # ログイン中の教員アカウントIDをセッションから取得
    # teacher_id = session.get('teacher_id')

    teacher_id = '111111'

    # 教員情報を取得し、担当クラス番号を取得
    teacher = Teacher.query.get(teacher_id)
    if not teacher:
        return "教員情報が見つかりません", 404
    
    # クラスごとに生徒を分類し、辞書形式で保持
    class_students = {}
    for student in Student.query.filter_by(class_num=teacher.class_num).all():
        class_num = student.class_num
        if class_num not in class_students:
            class_students[class_num] = []
        class_students[class_num].append(student)

    return render_template('teacher_student/class_list.html', class_students=class_students)