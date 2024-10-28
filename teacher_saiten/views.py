from flask import Blueprint, render_template, redirect, url_for
from app import db

saiten = Blueprint(
    "saiten",
    __name__,
    template_folder="templates",
    static_folder="static",
)
