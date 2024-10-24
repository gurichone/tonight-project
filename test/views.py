from flask import Blueprint, render_template, redirect, url_for, current_app
from gemini.forms import GeminiForms, UploadImageForm, JupyterForms
from pathlib import Path
from gemini.models import Codes
from app import db

#Blueprint currydar_app
#アプリを生成する
test = Blueprint(
    "menu",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@test.route("/")
def testDAO():
    return "testDAO"