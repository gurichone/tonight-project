from app import db 
from auth.models import Teacher, Student 
from flask import Blueprint, flash, redirect, render_template, request, url_for

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")