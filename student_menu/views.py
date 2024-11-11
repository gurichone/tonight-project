from flask import Blueprint, render_template, redirect, url_for
from app import db


menu = Blueprint(
    "menu",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@menu.route("/")
def s_menu():
    return render_template('student_menu/menu.html')