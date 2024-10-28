from flask import Blueprint, render_template, redirect, url_for, request
from app import db

send = Blueprint(
    "send",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@send.route("/")
def teacher_send():
    return "send"