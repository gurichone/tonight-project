from flask import Blueprint, render_template, redirect, url_for, current_app
from gemini.forms import GeminiForms, UploadImageForm, JupyterForms
from pathlib import Path
from gemini.models import Codes
from app import db
import uuid
import google.generativeai as genai
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

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

# テキストエリアで与えられたテストケースを二重リストに変換
def make_testcase(txt):
    txt = txt.split("\r\n")
    testcases = list()
    testcase = list()
    for t in txt:
        if t == "{% end %}":
            testcases.append(testcase)
            testcase = list()
        else:
            testcase.append(t)
    return testcases
    


@gemini.route('/', methods=["GET", "POST"])
def gemini_app(): 
    # aaa = db.session.query(Codes).delete()
    # db.session.commit()
    form = GeminiForms() # currydar/forms.pyのEventFormクラスを使えるようにする
    codes = db.session.query(Codes).all()
    form.code.choices = [(code.id, code.code_name)for code in codes]
    if form.validate_on_submit(): # フォームが正しく入力されているかをチェック
        code = db.session.query(Codes).get(form.code.data)
        file_path = Path(current_app.config["UPLOAD_FOLDER"], code.code_path)
        with open(file_path, encoding="utf-8") as f:
            txt = f.read()
        # Google Generative AI（Gemini API）のAPIキー設定
        genai.configure(api_key="AIzaSyAx46slXSnBOfnkCFK3MlKNnmoDuziwrpU")
        # Geminiモデルの設定
        model = genai.GenerativeModel('gemini-pro')
        # セッション状態にメッセージリストがない場合は初期化
        prompt = form.question.data + gemini_syntax + txt
        response = model.generate_content(prompt)
        # 応答をテキストとして取得（ここではresponse.textと仮定）
        assistant_response = response.text
        
        return render_template("gemini/output.html", ans=assistant_response)
        
    return render_template("gemini/input.html", form=form)

@gemini.route('/jupyter', methods=["GET", "POST"])
def jupyter_app(): 
    form = JupyterForms() # Formクラスを使えるようにする
    # コードの選択肢を更新
    codes = db.session.query(Codes).all()
    form.code.choices = [(code.id, code.code_name)for code in codes]
    if form.validate_on_submit(): # フォームが正しく入力されているかをチェック
        # コードを取得
        code = db.session.query(Codes).get(form.code.data)
        stdin = make_testcase(form.stdin.data) # 入力を取得
        stdout = make_testcase(form.stdout.data) # 出力を取得
        if len(stdin) != len(stdout):
            return render_template("gemini/error.html") # 入力と出力の数が違ったらエラー
        results = list() # htmlに送るやつ
        for i in range(len(stdin)):
            results.append({"stdin":stdin[i], "stdout":stdout[i], "ans":list(), "ox":False})
        # ファイル読み込み
        file_path = Path(current_app.config["UPLOAD_FOLDER"], code.code_path)
        with open(file_path, encoding="utf-8") as f:
            basetxt = f.read()
        # r1つ＝テストケース1つ
        for r in results:
            # コードのコピーを作成
            txt = basetxt
            count = 0
            # input()を置換
            while txt.count("input()") > 0:
                if len(r["stdin"]) > count:
                    s = r["stdin"][count]
                else:
                    s = ""
                txt = txt.replace("input()", "\""+s+"\"", 1)
                count += 1
            # 空のjupyter notebook読み込み
            with open(Path(current_app.config["JUPYTER_FOLDER"], "in.ipynb")) as f:
                nb = nbformat.read(f, as_version=4)
            # 空のjupyter notebookに読み込んだコードを書きこむ
            nb['cells'][0]['source'] += ("\n" + txt)
            try:
                # 実行
                ep = ExecutePreprocessor(timeout=500)
                ep.preprocess(nb,resources={'metadata': {'path': '/'}})
                # 実行後のjupyter notebookを保存
                with open(Path(current_app.config["JUPYTER_FOLDER"], "out.ipynb"), "w") as f:
                    nbformat.write(nb, f)
                    
                # 実行結果の部分だけを抽出
                ans = nb['cells'][0]['outputs'][0]['text']
            except:
                ans="error\n"
            r["ans"] = ans.split("\n")[:-1]

            # 正誤判定
            if len(r["stdout"]) == len(r["ans"]):
                r["ox"] = True
                for i in range(len(r["stdout"])):
                    if r["stdout"][i] != r["ans"][i]:
                        r["ox"] = False
                        break

        return render_template("gemini/file.html", results = results)
        
    num = db.session.query(Codes).count()
    return render_template("gemini/jupyter.html", form=form, num=num)

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