from flask import Blueprint, render_template, redirect, url_for
from app import db


enquete = Blueprint(
    "enquete",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@enquete.route("/")
def s_enquete():
    return "enquete"