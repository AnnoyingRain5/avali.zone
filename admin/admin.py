from flask import Blueprint, render_template, request, redirect, Response, flash
from werkzeug.exceptions import BadRequest
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


@auth.requires_auth(["admin"])
@admin.route("/infoboxes")
def infobox_manage():
    headers = db.get_db().execute("PRAGMA table_info(infoboxes)").fetchall()
    infoboxes = (
        db.get_db()
        .execute("SELECT * FROM infoboxes ORDER BY type, displayorder")
        .fetchall()
    )
    return render_template(
        "list.jinja", items=infoboxes, headers=headers, type="infoboxes"
    )


@auth.requires_auth(["admin"])
@admin.route("/infoboxes/create")
def infobox_create():
    return render_template("infobox_create.jinja")


@auth.requires_auth(["admin"])
@admin.route("/infoboxes/create/submit", methods=["post"])
def infobox_create_submit():
    database = db.get_db()
    database.execute(
        "INSERT INTO infoboxes (name, type, description, categoryid, owner, displayorder) VALUES (?, ?, ?, ?, ?, ?);",
        (
            request.form["name"],
            request.form["type"],
            request.form["description"],
            request.form["categoryid"],
            request.form["owner"],
            request.form["displayorder"],
        ),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@auth.requires_auth(["admin"])
@admin.route("/links")
def links_list():
    headers = db.get_db().execute("PRAGMA table_info(links)").fetchall()
    infoboxes = db.get_db().execute("SELECT * FROM links").fetchall()
    return render_template("list.jinja", items=infoboxes, headers=headers, type="links")


@auth.requires_auth(["admin"])
@admin.route("/categories")
def categories_manage():
    headers = db.get_db().execute("PRAGMA table_info(categories)").fetchall()
    infoboxes = (
        db.get_db()
        .execute("SELECT * FROM categories ORDER BY type, displayorder")
        .fetchall()
    )
    return render_template(
        "list.jinja", items=infoboxes, headers=headers, type="categories"
    )


@auth.requires_auth(["admin"])
@admin.route("/categories/create")
def category_create():
    return render_template("category_create.jinja")


@auth.requires_auth(["admin"])
@admin.route("/categories/create/submit", methods=["post"])
def category_create_submit():
    database = db.get_db()
    database.execute(
        "INSERT INTO categories (name, displayorder, type) VALUES (?, ?, ?);",
        (request.form["name"], request.form["displayorder"], request.form["type"]),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@auth.requires_auth(["admin"])
@admin.route("/infoboxes/<int:id>/edit")
def infobox_edit(id):
    links = db.get_db().execute("SELECT * FROM links WHERE infoboxid = ?", (id,))
    infobox = (
        db.get_db().execute("SELECT * FROM infoboxes WHERE id = ?", (id,)).fetchall()
    )
    return render_template("infobox_edit.jinja", infobox=infobox, links=links)


@auth.requires_auth(["admin"])
@admin.route("/categories/<int:id>/edit")
def category_edit(id):
    category = (
        db.get_db().execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchall()
    )
    return render_template("category_edit.jinja", category=category)


@auth.requires_auth(["admin"])
@admin.route("/categories/<int:id>/edit/submit", methods=["post"])
def category_edit_submit(id):
    database = db.get_db()
    database.execute(
        "UPDATE categories SET name = ?, type = ?, displayorder = ? WHERE id = ?;",
        (request.form["name"], request.form["type"], request.form["displayorder"], id),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@auth.requires_auth(["admin"])
@admin.route("/infoboxes/<int:id>/edit/submit", methods=["post"])
def infobox_edit_submit(id):
    database = db.get_db()
    database.execute(
        "UPDATE infoboxes SET name = ?, type = ?, description = ?, categoryid = ?, owner = ?, displayorder = ? WHERE id = ?;",
        (
            request.form["name"],
            request.form["type"],
            request.form["description"],
            request.form["categoryid"],
            request.form["owner"],
            request.form["displayorder"],
            id,
        ),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@auth.requires_auth(["admin"])
@admin.route("/links/<int:id>/edit/submit", methods=["post"])
def link_edit_submit(id):
    database = db.get_db()
    database.execute(
        "UPDATE links SET name = ?, destination = ? WHERE id = ?;",
        (request.form["name"], request.form["destination"], id),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@auth.requires_auth(["admin"])
@admin.route("/links/create/submit", methods=["post"])
def link_create_submit():
    infoboxid = None
    if request.form.get("infoboxid", None):
        infoboxid = request.form["infoboxid"]
    elif request.args.get("infoboxid", None):
        infoboxid = request.args["infoboxid"]
    else:
        raise BadRequest
    database = db.get_db()
    database.execute(
        "INSERT INTO links (name, destination, infoboxid) VALUES (?, ?, ?)",
        (request.form["name"], request.form["destination"], infoboxid),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)
