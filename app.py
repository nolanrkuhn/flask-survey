from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
toolbar = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    return render_template('start.html', survey=satisfaction_survey)

@app.route('/start', methods=['POST'])
def start_survey():
    session['responses'] = []
    return redirect(url_for('question_page', qid=0))

@app.route('/questions/<int:qid>')
def question_page(qid):
    responses = session.get('responses', [])
    if qid != len(responses):
        flash("Invalid question number. Please answer the questions in order.")
        return redirect(url_for('question_page', qid=len(responses)))
    
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', survey=satisfaction_survey, question=question, qid=qid)

@app.route('/answer/<int:qid>', methods=['POST'])
def handle_answer(qid):
    responses = session.get('responses', [])
    answer = request.form['answer']
    responses.append(answer)
    session['responses'] = responses
    
    next_qid = qid + 1
    if next_qid < len(satisfaction_survey.questions):
        return redirect(url_for('question_page', qid=next_qid))
    else:
        return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html', survey=satisfaction_survey)

if __name__ == "__main__":
    app.run(debug=True)
