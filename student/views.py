from flask import Blueprint, render_template, redirect, url_for
from app import db


student = Blueprint(
    "student",
    __name__,
    template_folder="templates",
    static_folder="static",
)


from student_menu import views as student_menu_views
student.register_blueprint(student_menu_views.menu, url_prefix="/")

from student_syusseki import views as student_syusseki_views
student.register_blueprint(student_syusseki_views.syusseki, url_prefix="/syusseki")

from student_todo import views as student_todo_views
student.register_blueprint(student_todo_views.todo, url_prefix="/todo")

from student_seiseki import views as student_seiseki_views
student.register_blueprint(student_seiseki_views.seiseki, url_prefix="/seiseki")

from student_teisyutsu import views as student_teisyutsu_views
student.register_blueprint(student_teisyutsu_views.teisyutsu, url_prefix="/teisyutsu")

from student_jikanwari import views as student_jikanwari_views
student.register_blueprint(student_jikanwari_views.jikanwari, url_prefix="/jikanwari")

from student_enquete import views as student_enquete_views
student.register_blueprint(student_enquete_views.enquete, url_prefix="/enquete")