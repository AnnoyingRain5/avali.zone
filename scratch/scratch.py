import json
import random
import werkzeug
from flask import render_template, Blueprint, abort, request

with open("static/json/wordlist.json") as f:
    wordlist = json.load(f)["wordlist"]

scratch = Blueprint(
    "scratch", __name__, template_folder="templates", url_prefix="/scratch"
)


@scratch.route("/")
def index():
    return render_template("scratch/index.jinja")


@scratch.route("/resources")
def resources():
    return render_template("scratch/resources.jinja")


@scratch.route("/practice/<practice_type>")
def practice_word(practice_type: str):
    if practice_type in ["word", "letter"]:
        pb = 0
        try:
            pb = request.cookies[f"score-pb-{practice_type}"]
        except KeyError:
            pass
        return render_template(
            "scratch/practice.jinja",
            practicetype=practice_type.title(),
            pb=pb
        )
    else:
        abort(404)


@scratch.route("/internal/Word-sub")
def word_practice_sub():
    while True:
        prompt = random.choice(wordlist)
        last_prompt = None
        try:
            last_prompt = request.cookies["lastprompt"]
        except KeyError:
            pass
        if prompt != last_prompt:
            break
    answers = [prompt]
    for _ in range(2):
        while True:
            temp_answer = random.choice(wordlist)
            if temp_answer not in answers:
                answers.append(temp_answer)
                break
    answers.sort()
    return render_template(
        (
            "scratch/practice-input-sub.jinja"
            if random.randint(0, 1)
            else "scratch/practice-prompt-sub.jinja"
        ),
        prompt=prompt,
        answers=answers,
        practicetype="Word",
    )


@scratch.route("/internal/Letter-sub")
def letter_practice_sub():
    while True:
        prompt = chr(random.choice(list(range(65, 91)) + list(range(48, 58))))
        last_prompt = None
        try:
            last_prompt = request.cookies["lastprompt"]
        except KeyError:
            pass
        if prompt != last_prompt:
            break
    answers = [prompt]
    for _ in range(2):
        while True:
            temp_answer = chr(random.randint(65, 90))
            if temp_answer not in answers:
                answers.append(temp_answer)
                break
    answers.sort()
    return render_template(
        (
            "scratch/practice-input-sub.jinja"
            if random.randint(0, 1)
            else "scratch/practice-prompt-sub.jinja"
        ),
        prompt=prompt,
        answers=answers,
        practicetype="Letter",
    )


@scratch.route("/<first>")
@scratch.route("/<first>/<path:rest>")
def catchall(first=None, rest=None):
    abort(404)


@scratch.errorhandler(werkzeug.exceptions.HTTPException)
def error(error: werkzeug.exceptions.HTTPException):
    return render_template("scratch/error.jinja", error=error)
