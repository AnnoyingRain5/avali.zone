from flask import Blueprint, render_template, request, redirect, Response
import json
import db
import auth

admin = Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")


@admin.route("/users")
@auth.requires_auth(["admin"])
def user_list(user, userinfo):
    headers = db.get_db().execute("PRAGMA table_info(USERS)").fetchall()
    users = db.get_db().execute("SELECT * FROM USERS").fetchall()
    return render_template("list.jinja", items=users, headers=headers, type="user")

@auth.requires_auth(["admin"])
@admin.route("/golinks")
def golink_list():
    headers = db.get_db().execute("PRAGMA table_info(golinks)").fetchall()
    golinks = db.get_db().execute("SELECT * FROM golinks").fetchall()
    return render_template("list.jinja", items=golinks, headers=headers, type="golink")

