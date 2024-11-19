from flask import Blueprint, render_template, redirect, url_for
from app import db


notice = Blueprint(
    "notice",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@notice.route("/")
def s_notice():
    return "notice"