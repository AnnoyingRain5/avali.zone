from flask import redirect, Blueprint, request
import os

util = Blueprint("util", __name__, template_folder="templates", url_prefix="/util")


@util.route("/togglelang")
def togglelang():
    if request.referrer != None:
        resp = redirect(request.referrer)
    else:
        resp = redirect("/")
    if request.cookies.get("fontchoice", "scratch") == "english":
        resp.set_cookie("fontchoice", "scratch", max_age=31536000)
    else:
        resp.set_cookie("fontchoice", "english", max_age=31536000)
    return resp
