from flask import render_template, session, redirect, request, Flask, flash
import surveys

app = Flask(__name__)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = 'nimdA'

@app.route("/")
def show_home_page():
    if not session.get('c_qid'):
        session["c_qid"] = 0
        session["responses"] = []
        return render_template("home.html")
    elif session["c_qid"] < len(surveys.satisfaction_survey.questions):
        flash("Returning you to your unfinished survey")
        return redirect(f"/question/{session['c_qid']}")
    #This return will only be reached if user attempts to redo the survey after completing it.
    return redirect("/finished")

@app.route("/question/<q_number>")
def show_question_page(q_number):
    #check if current question is actually past the last one, then render a different page
    
    if int(q_number) != session["c_qid"]:
        flash("Invalid question id / Havent completed earlier questions")
        return redirect(f"/question/{session['c_qid']}")
    if str(len(surveys.satisfaction_survey.questions)) == q_number:
        return redirect("/finished")
    c_question = surveys.satisfaction_survey.questions[int(q_number)]
    return render_template(
        "questions.html",
        question_number=str(int(q_number) + 1),
        question=c_question.question,
        choices=c_question.choices,
        redirect_link=str(int(q_number) + 1),
    )

@app.route("/answer", methods=["POST"])
def get_answer():
    session["responses"].append(request.form["answer"])
    session["c_qid"] += 1
    return redirect(f"/question/{session['c_qid']}")

@app.route("/finished")
def show_finished_page():
    return render_template("finished.html")