from flask import Blueprint, render_template, redirect, url_for
from app import db


seiseki = Blueprint(
    "seiseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@seiseki.route("/")
def s_seiseki():
    return "seiseki"