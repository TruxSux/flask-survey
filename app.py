import flask
import surveys

app = flask.Flask(__name__)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["SECRET_KEY"] = 'nimdA'
responses = []
c_qid = 0


@app.route("/")
def show_home_page():
    global c_qid
    global responses
    c_qid = 0
    responses = []
    return flask.render_template("home.html")


@app.route("/question/<q_number>")
def show_question_page(q_number):
    global c_qid
    #check if current question is actually past the last one, then render a different page
    
    if int(q_number) != c_qid:
        flask.flash("Invalid question id / Havent completed earlier questions")
        return flask.redirect(f"/question/{c_qid}")
    if str(len(surveys.satisfaction_survey.questions)) == q_number:
            return flask.redirect("/finished")
    c_question = surveys.satisfaction_survey.questions[int(q_number)]
    return flask.render_template(
        "questions.html",
        question_number=str(int(q_number) + 1),
        question=c_question.question,
        choices=c_question.choices,
        redirect_link=str(int(q_number) + 1),
    )

@app.route("/answer", methods=["POST"])
def get_answer():
    global c_qid
    responses.append(flask.request.form["answer"])
    c_qid += 1
    return flask.redirect(f"/question/{c_qid}")

@app.route("/finished")
def show_finished_page():
    return flask.render_template("finished.html")