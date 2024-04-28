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
    return render_template("user_list.jinja", users=users, headers=headers)


