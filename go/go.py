from flask import Blueprint, redirect, request, render_template, url_for, current_app
from flask_dance.contrib.google import google
import sys
import sqlite3
sys.path.append("..") 
import db
import auth
go = Blueprint("go", __name__, template_folder="templates", url_prefix="/go")

@go.route('/', methods=["GET", "POST"])
@auth.requires_auth(["golink"])
def create_golink(userinfo, user):
    if request.method == "GET":
        return render_template("create_golink.jinja", userinfo=userinfo)
    else:
        # it's a POST request!
        if not request.form["location"].startswith("https://"):
            if not request.form["location"].startswith("http://"):
                return "I'm afraid that's not a valid destination address"
        database = db.get_db()
        try:
            database.execute("INSERT INTO golinks VALUES (?, ?, ?)", (request.form["golink"], request.form["location"], f"GOOGLE_{userinfo['email']}"))
            database.commit()
        except sqlite3.IntegrityError:
            return "This golink has already been used!"
        return render_template("golink_success.jinja", golink=request.form["golink"])
    
@go.route("/<golink>")
def _go(golink: str):
    database = db.get_db()
    golink = database.execute("SELECT * FROM golinks WHERE name = ?", (golink,)).fetchone()
    if golink:
        return redirect(golink["destination"])
    else:
        return "Invalid golink"
