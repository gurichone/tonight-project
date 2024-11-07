from flask import Blueprint, render_template, redirect, url_for
from app import db


teisyutsu = Blueprint(
    "teisyutsu",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@teisyutsu.route("/")
def s_teisyutsu():
    return "teisyutsu"