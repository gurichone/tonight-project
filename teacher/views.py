from flask import Blueprint, render_template, redirect, url_for
from app import db

#Blueprint currydar_app
#アプリを生成する
teacher = Blueprint(
    "teacher",
    __name__,
    template_folder="templates",
    static_folder="static",
)


from teacher_menu import views as teacher_menu_views
teacher.register_blueprint(teacher_menu_views.menu, url_prefix="/")

from teacher_student import views as teacher_student_views
teacher.register_blueprint(teacher_student_views.student, url_prefix="/student")

from teacher_seiseki import views as teacher_seiseki_views
teacher.register_blueprint(teacher_seiseki_views.seiseki, url_prefix="/seiseki")

from teacher_teisyutsu import views as teacher_teisyutsu_views
teacher.register_blueprint(teacher_teisyutsu_views.teisyutsu, url_prefix="/teisyutsu")

from teacher_jikanwari import views as teacher_jikanwari_views
teacher.register_blueprint(teacher_jikanwari_views.jikanwari, url_prefix="/jikanwari")

from teacher_saiten import views as teacher_saiten_views
teacher.register_blueprint(teacher_saiten_views.saiten, url_prefix="/saiten")

from teacher_chat import views as teacher_chat_views
teacher.register_blueprint(teacher_chat_views.chat, url_prefix="/chat")

from teacher_notice import views as teacher_notice_views
teacher.register_blueprint(teacher_notice_views.notice, url_prefix="/notice")

from teacher_sent import views as teacher_sent_views
teacher.register_blueprint(teacher_sent_views.sent, url_prefix="/sent")