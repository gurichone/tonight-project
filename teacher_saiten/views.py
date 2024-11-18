from flask import Blueprint, render_template, redirect, url_for, session, current_app, send_file
from flask_login import current_user, login_required
from app import db
from teacher_saiten.forms import PointForm
from teacher_teisyutsu.models import Submission, Personal_Submission
from auth.models import Subject, Student
import shutil
from pathlib import Path
import copy
import google.generativeai as genai
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def jupyter(testcase, lst, codes):
    testcase = testcase.split("\r\n")
    test = {"input":list(), "output":list(), "ans":list(), "ox":False}
    baseout = list()
    txt = list()
    next = 0
    for t in testcase:
        if next == 0:
            if t == "<<<start>>>":
                next = 1
                test = {"input":list(), "output":list(), "ans":list(), "ox":False}
        elif next == 1:
            if t == "<<<change>>>":
                next = 2
            else:
                test["input"].append(t)
        elif next == 2:
            if t == "<<<end>>>":
                baseout.append(test)
                next = 0
            else:
                test["output"].append(t)
    output = dict()
    
    for l in lst:

        if l.Personal_Submission.submitted:
            point = len(baseout)
            result = copy.deepcopy(baseout)
            basetxt = codes[l.Student.id]
            for r in result:
            # ファイル読み込み
            # r1つ＝テストケース1つ    
            # コードのコピーを作成
                txt = basetxt
                count = 0
                # input()を置換
                while txt.count("input()") > 0:
                    if len(r["input"]) > count:
                        s = r["input"][count]
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
                    ans = "error\n"
                r["ans"] = ans.split("\n")[:-1]

                # 正誤判定
                if len(r["output"]) == len(r["ans"]):
                    r["ox"] = True
                    for i in range(len(r["output"])):
                        if r["output"][i] != r["ans"][i]:
                            r["ox"] = False
                            point -= 1
                            break
        else:
            result = False
            point = 0
        # 最後に得点と学生IDをいれるように変更
        if len(baseout) > 0:
            output[l.Student.id] = {"result":result, "point":(point*100) // len(baseout)}
        else:
            output[l.Student.id] = {"result":result, "point":0}
    return output


def gemini(question, lst, codes):
    gemini_syntax = """
    という問題に対して以下のコードを書きましたpythonで書きました。
    このコードを評価し、100点満点で点数をつけて点数のみを出力して
    """
    output = dict()
    # file_path = Path(current_app.config["UPLOAD_FOLDER"], code.code_path)
    # with open(file_path, encoding="utf-8") as f:
    #     txt = f.read()
    # Google Generative AI（Gemini API）のAPIキー設定
    # genai.configure(api_key="AIzaSyAx46slXSnBOfnkCFK3MlKNnmoDuziwrpU")
    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
    # Geminiモデルの設定
    model = genai.GenerativeModel('gemini-pro')
    for l in lst:
        if l.Personal_Submission.submitted:
            txt = codes[l.Student.id]
            # セッション状態にメッセージリストがない場合は初期化
            prompt = question + gemini_syntax + txt
            response = model.generate_content(prompt)
            # 応答をテキストとして取得（ここではresponse.textと仮定）
            assistant_response = response.text.split("\n")

            # 文字列整理 
            ans = ""
            for a in assistant_response[0]:
                if a in "0123456789":
                    ans+=a
            # codeflag = False
            # for a in assistant_response:
            #     if len(a) == 0:
            #         continue
            #     if codeflag and a[-3:] == "```":
            #         ans.append({"class":"endcode", "txt":a[:-3]})
            #     elif a[0] == "*":
            #         if a[1] == "*":
            #             ans.append({"class":"head", "txt":a})
            #         else:
            #             ans.append({"class":"text", "txt":a})
            #     elif a[0:3] == "```":
            #         codeflag = True
            #         ans.append({"class":"code", "txt":a[3:]})
            #     else:
            #         ans.append({"class":"text", "txt":a})
        else:
            ans = "0"
        output[l.Student.id] = {"result":int(ans)}
    return output

saiten = Blueprint(
    "saiten",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@saiten.route("/<submission_id>/")
@login_required
def t_saiten(submission_id):
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission = db.session.query(Submission, Subject).join(Submission, Submission.subject_id==Subject.subject_id).filter_by(submission_id=submission_id).first()
    personal = db.session.query(Personal_Submission, Student).join(Personal_Submission, Personal_Submission.student_id==Student.id).filter_by(submission_id=submission_id).all()
    session["submission"] = submission_id
    return render_template("teacher_saiten/index.html", submission=submission, personal=personal)

@saiten.route("/manual")
@login_required
def manual():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission = db.session.query(Submission, Subject).join(Submission, Submission.subject_id==Subject.subject_id).filter_by(submission_id=session["submission"]).first()
    filename=submission.Submission.submission_name
    shutil.make_archive(filename, format="zip", root_dir=Path(current_app.config["SUBMIT_FOLDER"]), base_dir=Path(str(submission.Submission.submission_id)))
    return send_file(filename + ".zip")

@saiten.route("/auto", methods=["GET", "POST"])
@login_required
def auto():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission = db.session.query(Submission, Subject).join(Submission, Submission.subject_id==Subject.subject_id).filter_by(submission_id=session["submission"]).first()
    personal_lst = db.session.query(Personal_Submission, Student).join(Personal_Submission, Personal_Submission.student_id==Student.id).filter_by(submission_id=session["submission"]).all()
    form = PointForm()
    if form.validate_on_submit():
        key = False
        for f in form.fieldlist.data.split("\r\n"):
            if key:
                personal = db.session.query(Personal_Submission).filter_by(student_id=key).first()
                personal.point = f
                db.session.add(personal)
                db.session.commit()
                key = False
            else:
                key = f
        return render_template("teacher_saiten/done.html", submission=submission)
    codes = dict()
    points = dict()
    for pl in personal_lst:
        if pl.Personal_Submission.submitted:
            file_path = Path(current_app.config["SUBMIT_FOLDER"], pl.Personal_Submission.file)
            with open(file_path, encoding="utf-8") as f:
                codes[pl.Student.id] = f.read()
    if submission.Submission.scoring_type == 1:
        jupyter_output = jupyter(submission.Submission.testcase, personal_lst, codes)
        gemini_output = False
        for p in personal_lst:
            points[p.Student.id]=jupyter_output[p.Student.id]["point"]
    elif submission.Submission.scoring_type == 2:
        jupyter_output = False
        gemini_output = gemini(submission.Submission.question, personal_lst, codes)
        for p in personal_lst:
            points[p.Student.id]=gemini_output[p.Student.id]["result"]
    elif submission.Submission.scoring_type == 3:
        jupyter_output = jupyter(submission.Submission.testcase, personal_lst, codes)
        gemini_output = gemini(submission.Submission.question, personal_lst, codes)
        for p in personal_lst:
            points[p.Student.id]=(jupyter_output[p.Student.id]["point"]+gemini_output[p.Student.id]["result"])//2
    else:
        jupyter_output = False
        gemini_output = False
    for pl in personal_lst:
        if pl.Personal_Submission.submitted:
            codes[pl.Student.id]=codes[pl.Student.id].split("\n")
    return render_template("teacher_saiten/result.html", jupyter=jupyter_output, gemini=gemini_output, personal_lst=personal_lst, codes=codes, form=form, points=points, submission=submission)
    # return render_template("teacher_saiten/index.html")
