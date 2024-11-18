from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_migrate import Migrate

login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.loginmessage = ""     

db = SQLAlchemy()

def create_app(config_name="local"):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    from auth import views as auth_views # auth/views.pyをauth_viewsという名前で使用
    app.register_blueprint(auth_views.auth, url_prefix="/") # auth_viewsのauthとurl"/auth"を紐づけ

    from teacher import views as teacher_views
    app.register_blueprint(teacher_views.teacher, url_prefix="/teacher")

    from student import views as student_views
    app.register_blueprint(student_views.student, url_prefix="/student")

    from gemini import views as gemini_views # gemini/views.pyをgemini_viewsという名前で使用
    app.register_blueprint(gemini_views.gemini, url_prefix="/gemini") # gemini_viewsのgeminiとurl"/gemini"を紐づけ
    
    from admin import views as admin_views
    app.register_blueprint(admin_views.admin, url_prefix="/admin")

    return app
