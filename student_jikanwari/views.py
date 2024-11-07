from flask import Blueprint, render_template, redirect, url_for
from app import db


jikanwari = Blueprint(
    "jikanwari",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@jikanwari.route("/")
def s_jikanwari():
    return "jikanwari"