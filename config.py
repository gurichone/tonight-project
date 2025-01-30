from pathlib import Path

basedir = Path(__file__).parent # baseディレクトリの指定(appsフォルダ)

class BaseConfig:
    SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
    WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    # GEMINI_API_KEY = "AIzaSyCYErBLD7yQiZwvxfrFZdpfz150GoR6VE8"
    GEMINI_API_KEY = "AIzaSyAe9GNoI-W-THApcwrObbRWgArK2B1o79Y"
    SQLALCHEMY_ECHO=True
    
    MAIL_SERVER="smtp.gmail.com"
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME="kotatsu.10y@gmail.com"
    MAIL_PASSWORD="sloz ekrj abzy vrhv"
    MAIL_DEFAULT_SENDER="Flaskbook <kotatsu.10y@gmail.com>"


# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # 画像アップロード先にmedia/imagesを指定する
    UPLOAD_FOLDER = "codes"
    JUPYTER_FOLDER = "jupyter"
    SUBMIT_FOLDER = "submit"
    DOWNLOAD_PATH = ""


# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    # 画像アップロード先にmedia/imagesを指定する
    UPLOAD_FOLDER = str(Path(basedir,"codes"))
    JUPYTER_FOLDER = str(Path(basedir,"jupyter"))
    SUBMIT_FOLDER = str(Path(basedir,"submit"))
    DOWNLOAD_PATH = Path(__file__).parent


# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}
