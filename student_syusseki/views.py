from flask import Blueprint, render_template, redirect, url_for
from app import db


syusseki = Blueprint(
    "syusseki",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@syusseki.route("/")
def s_syusseki():
    return "syusseki"