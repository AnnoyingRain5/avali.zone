from flask import redirect, render_template, Blueprint, abort, request

util = Blueprint("util", __name__, template_folder="templates", subdomain="", url_prefix="/util")

@util.route("/togglelang")
def togglelang():
    print(request.referrer)
    if request.referrer != None:
        resp = redirect(request.referrer)
    else:
        resp = redirect("/")
    if request.cookies.get("english", False):
        resp.delete_cookie("english")
    else:
        resp.set_cookie("english", "True")
    return resp
