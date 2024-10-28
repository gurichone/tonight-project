from flask import Blueprint, render_template, redirect, url_for, request
from app import db

sent = Blueprint(
    "sent",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@sent.route("/")
def teacher_sent():
    return "sent"