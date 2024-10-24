from flask import Blueprint, render_template, redirect, url_for, current_app
from gemini.forms import GeminiForms, UploadImageForm, JupyterForms
from pathlib import Path
from gemini.models import Codes
from app import db

#Blueprint currydar_app
#アプリを生成する
teacher = Blueprint(
    "teacher",
    __name__,
    template_folder="templates",
    static_folder="static",
)

from test import views as test_views
teacher.register_blueprint(test_views.test, url_prefix="/test")

@teacher.route("/")
def teacherDAO():
    return "teacherDAO"