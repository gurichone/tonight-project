from flask import Blueprint, render_template, redirect, url_for, current_app
from gemini.forms import GeminiForms, UploadImageForm
from pathlib import Path
from gemini.models import Codes
from app import db
import uuid
import google.generativeai as genai

#Blueprint currydar_app
#アプリを生成する
gemini = Blueprint(
    "gemini",
    __name__,
    template_folder="templates",
    static_folder="static",
)

gemini_syntax = """
という問題に対して以下のコードを書きましたpythonで書きました。
このコードを評価し、100点満点で点数をつけてください。
また100点だと言えるコードを出力してください。"""



@gemini.route('/', methods=["GET", "POST"])
def gemini_app(): 
    form = GeminiForms() # currydar/forms.pyのEventFormクラスを使えるようにする
    if form.validate_on_submit(): # フォームが正しく入力されているかをチェック
        # Google Generative AI（Gemini API）のAPIキー設定
        genai.configure(api_key="AIzaSyAx46slXSnBOfnkCFK3MlKNnmoDuziwrpU")
        # Geminiモデルの設定
        model = genai.GenerativeModel('gemini-pro')
        # セッション状態にメッセージリストがない場合は初期化
        prompt = form.question.data + gemini_syntax + form.code.data 
        response = model.generate_content(prompt)
        # 応答をテキストとして取得（ここではresponse.textと仮定）
        assistant_response = response.text
        print(assistant_response)
        return render_template("gemini/output.html", ans=assistant_response)
    codes = db.session.query(Codes).all()
    form.code.choices = [(code.id, code.code_name)for code in codes]
    return render_template("gemini/input.html", form=form)

@gemini.route("/upload", methods=["GET", "POST"])
def upload_code():
    form = UploadImageForm()
    if form.validate_on_submit():
        file = form.code.data
        #拡張子を抽出
        ext = Path(file.filename).suffix
        code_uuid_file_name = str(uuid.uuid4()) + ext

        code_path =Path(
            current_app.config["UPLOAD_FOLDER"], code_uuid_file_name
            )
        print(current_app.config["UPLOAD_FOLDER"])
        file.save(code_path)

        codes = Codes(
            code_name=file.filename,
            code_path=code_uuid_file_name
        )

        db.session.add(codes)
        db.session.commit()
        return redirect(url_for("gemini.gemini_app"))

    return render_template("gemini/upload.html", form=form)