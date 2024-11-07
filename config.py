from pathlib import Path

basedir = Path(__file__).parent # baseディレクトリの指定(appsフォルダ)

class BaseConfig:
    SECRET_KEY = "2AZSMss3p5QPbcY2hBsJ"
    WTF_CSRF_SECRET_KEY = "AuwzyszU5sugKN7KZs6f"
    OWM_API_KEY = "133181fd446d837a42413992c3e8b9e2"
    SQLALCHEMY_ECHO=True


# BaseConfigクラスを継承してLocalConfigクラスを作成する
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # 画像アップロード先にmedia/imagesを指定する
    UPLOAD_FOLDER = "codes"
    JUPYTER_FOLDER = "jupyter"
    SUBMIT_FOLDER = "submit"


# BaseConfigクラスを継承してTestingConfigクラスを作成する
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'testing.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    # 画像アップロード先にmedia/imagesを指定する
    UPLOAD_FOLDER = str(Path(basedir,"codes"))
    JUPYTER_FOLDER = str(Path(basedir,"jupyter"))
    SUBMIT_FOLDER = str(Path(basedir,"submit"))


# config辞書にマッピングする
config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}
