from flask import Blueprint, render_template, redirect, url_for, request
from app import db

chat = Blueprint(
    "chat",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@chat.route("/")
def teacher_chat():
    return "chat"