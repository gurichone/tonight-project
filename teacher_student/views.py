from flask import Blueprint, render_template, redirect, url_for, request
from app import db

student = Blueprint(
    "student",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@student.route("/")
def teacher_student():
    return render_template("stukanri.html")