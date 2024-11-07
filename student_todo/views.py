from flask import Blueprint, render_template, redirect, url_for
from app import db


todo = Blueprint(
    "todo",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@todo.route("/")
def s_todo():
    return "todo"