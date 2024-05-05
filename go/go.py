from flask import Blueprint, redirect, request, render_template, flash
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
        golinks = db.get_db().execute("SELECT name, destination FROM golinks WHERE owner = ?", (f"GOOGLE_{userinfo['email']}",)).fetchall()
        return render_template("create_golink.jinja", userinfo=userinfo, golinks=golinks)
    else:
        # it's a POST request!
        if not request.form["location"].startswith("https://"):
            if not request.form["location"].startswith("http://"):
                flash("I'm afraid that's not a valid destination address")
                redirect("/go")
        database = db.get_db()
        try:
            database.execute("INSERT INTO golinks VALUES (?, ?, ?)", (request.form["golink"], request.form["location"], f"GOOGLE_{userinfo['email']}"))
            database.commit()
        except sqlite3.IntegrityError:
            flash("This golink has already been used!", "error")
            return redirect("/go/")
        flash(f"Golink {request.form['golink']} created!", "success")
        return redirect("/go/")
    
@go.route("/<golink>")
def _go(golink: str):
    database = db.get_db()
    golink = database.execute("SELECT * FROM golinks WHERE name = ?", (golink,)).fetchone()
    if golink:
        return redirect(golink["destination"])
    else:
        flash("Invalid golink!")
        return redirect("/")


@go.route("/<golink>/delete")
@auth.requires_auth(["golink"])
def delete(golink: str, userinfo, user):
    database = db.get_db()
    db_golink = database.execute("SELECT * FROM golinks WHERE name = ?", (golink,)).fetchone()
    if golink:
        if db_golink["owner"] == f"GOOGLE_{userinfo['email']}" or auth.has_permission(user, "admin"):
            golink = database.execute("DELETE FROM golinks WHERE name = ?", (golink,)).fetchone()
            database.commit()
            flash(f"Golink {golink} deleted!", "success")
            return redirect(request.referrer)
    else:
        flash("Invalid golink!")
        return redirect("/")
