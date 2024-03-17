from flask import render_template, Blueprint, abort
import random
import werkzeug

scratch = Blueprint('scratch', __name__,
                        template_folder='templates/scratch')

@scratch.route('/')
def index():
    return render_template("scratch/index.jinja")

@scratch.route('/resources')
def resources():
    return render_template("scratch/resources.jinja")

@scratch.route("/practice/<practicetype>")
def practice_word(practicetype: str):
    if practicetype in ["word", "letter"]:
        return render_template("scratch/practice.jinja", practicetype=practicetype.title())
    else:
        abort(404)

@scratch.route("/internal/Word-sub")
def word_practice_sub():
    words = ["derg", "fluffy", "avali", "art", "scratch", "good", "letter", "word", "game", "fox", "key", "site", "practice", "status", "fair"]
    prompt = random.choice(words)
    answers = [prompt, random.choice(words), random.choice(words)]
    answers.sort()
    if random.randint(1,2) == 1:
        return render_template("scratch/practice-input-sub.jinja", prompt=prompt, answers=answers, practicetype="Word")
    else:
        return render_template("scratch/practice-prompt-sub.jinja", prompt=prompt, answers=answers, practicetype="Word")

@scratch.route("/internal/Letter-sub")
def letter_practice_sub():
    prompt = chr(random.randint(65, 90))
    answers = [prompt, chr(random.randint(65, 90)), chr(random.randint(65, 90))]
    answers.sort()
    if random.randint(1,2) == 1:
        return render_template("scratch/practice-input-sub.jinja", prompt=prompt, answers=answers, practicetype="Letter")
    else:
        return render_template("scratch/practice-prompt-sub.jinja", prompt=prompt, answers=answers, practicetype="Letter")

@scratch.errorhandler(werkzeug.exceptions.HTTPException)
def error(error: werkzeug.exceptions.HTTPException):
    return render_template("/scratch/error.jinja", error=error)