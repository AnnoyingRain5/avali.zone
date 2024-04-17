from flask import render_template, Blueprint, abort, request
import random
import json

import werkzeug

wordlist = []
with open("static/json/wordlist.json") as f:
    wordlist = json.load(f)["wordlist"]

scratch = Blueprint("scratch", __name__, template_folder="templates", subdomain="scratch")


@scratch.route("/")
def index():
    return render_template("scratch/index.jinja")


@scratch.route("/resources")
def resources():
    return render_template("scratch/resources.jinja")


@scratch.route("/practice/<practicetype>")
def practice_word(practicetype: str):
    if practicetype in ["word", "letter"]:
        return render_template(
            "scratch/practice.jinja", practicetype=practicetype.title()
        )
    else:
        abort(404)


@scratch.route("/internal/Word-sub")
def word_practice_sub():
    prompt = ""
    while True:
        prompt = random.choice(wordlist)
        lastprompt = None
        try:
            lastprompt = request.cookies["lastprompt"]
        except KeyError:
            pass
        if prompt != lastprompt:
            break
    answers = [prompt]
    for _ in range(2):
        while True:
            tempanswer = random.choice(wordlist)
            if tempanswer not in answers:
                answers.append(tempanswer)
                break
    answers.sort()
    if random.randint(1, 2) == 1:
        return render_template(
            "scratch/practice-input-sub.jinja",
            prompt=prompt,
            answers=answers,
            practicetype="Word",
        )
    else:
        return render_template(
            "scratch/practice-prompt-sub.jinja",
            prompt=prompt,
            answers=answers,
            practicetype="Word",
        )


@scratch.route("/internal/Letter-sub")
def letter_practice_sub():
    prompt = ""
    while True:
        prompt = chr(random.choice(list(range(65, 91)) + list(range(48, 58))))
        lastprompt = None
        try:
            lastprompt = request.cookies["lastprompt"]
        except KeyError:
            pass
        if prompt != lastprompt:
            break
    answers = [prompt]
    for _ in range(2):
        while True:
            tempanswer = chr(random.randint(65, 90))
            if tempanswer not in answers:
                answers.append(tempanswer)
                break
    answers.sort()
    if random.randint(1, 2) == 1:
        return render_template(
            "scratch/practice-input-sub.jinja",
            prompt=prompt,
            answers=answers,
            practicetype="Letter",
        )
    else:
        return render_template(
            "scratch/practice-prompt-sub.jinja",
            prompt=prompt,
            answers=answers,
            practicetype="Letter",
        )

@scratch.route('/<first>')
@scratch.route('/<first>/<path:rest>')
def catchall(first=None, rest=None):
    abort(404)

@scratch.errorhandler(werkzeug.exceptions.HTTPException)
def error(error: werkzeug.exceptions.HTTPException):
    return render_template("scratch/error.jinja", error=error)
