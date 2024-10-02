from flask import Blueprint, render_template, redirect, url_for
from gemini.forms import GeminiForms
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
        # return redirect(url_for("currydar.show_event")) # ユーザー一覧画面へリダイレクトする
    # フォームが正しく入力されていない場合はcrud/create.htmlに遷移
    return render_template("gemini/input.html", form=form)

