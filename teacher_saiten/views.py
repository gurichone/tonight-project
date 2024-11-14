from flask import Blueprint, render_template, redirect, url_for, session, current_app, send_file
from flask_login import current_user, login_required
from app import db
from teacher_teisyutsu.models import Submission, Personal_Submission
from auth.models import Subject, Student
import shutil
from pathlib import Path
import copy
import google.generativeai as genai
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def jupyter(testcase, lst):
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

        if l.Personal_Submission.file:
            point = len(baseout)
            result = copy.deepcopy(baseout)
            file_path = Path(current_app.config["SUBMIT_FOLDER"], l.Personal_Submission.file)
            with open(file_path, encoding="utf-8") as f:
                basetxt = f.read()
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
            basetxt=basetxt.split("\n")
        else:
            result = False
            point = 0
            basetxt = False
        output[l.Student.id] = {"result":result, "point":(point*100) // len(baseout), "code":basetxt}
    return output


def gemini():
    return

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

@saiten.route("/auto")
@login_required
def auto():
    if len(current_user.id) != 6:
        return render_template("teacher/gohb.html")
    submission = db.session.query(Submission, Subject).join(Submission, Submission.subject_id==Subject.subject_id).filter_by(submission_id=session["submission"]).first()
    personal_lst = db.session.query(Personal_Submission, Student).join(Personal_Submission, Personal_Submission.student_id==Student.id).filter_by(submission_id=session["submission"]).all()
    if submission.Submission.scoring_type == 1 or submission.Submission.scoring_type == 3:
        jupyter_output = jupyter(submission.Submission.testcase, personal_lst)
    if submission.Submission.scoring_type == 2 or submission.Submission.scoring_type == 3:
        jupyter_output = jupyter(submission.Submission.testcase, personal_lst)
    return render_template("teacher_saiten/result.html", jupyter=jupyter_output, personal_lst=personal_lst)