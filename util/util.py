from flask import redirect, Blueprint, request
import os

util = Blueprint("util", __name__, template_folder="templates", url_prefix="/util")

@util.route("/togglelang")
def togglelang():
    if request.referrer != None:
        resp = redirect(request.referrer)
    else:
        resp = redirect("/")
    if request.cookies.get("english", False):
        resp.delete_cookie("english")
    else:
        resp.set_cookie("english", "True")
    return resp
