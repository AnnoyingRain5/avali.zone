from flask import Blueprint, abort, render_template, request, redirect, flash

import auth
import db

admin = Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")


@admin.route("/users")
@auth.requires_auth(["admin"])
def user_list(user, userinfo):
    headers = db.get_db().execute("PRAGMA table_info(USERS)").fetchall()
    users = db.get_db().execute("SELECT * FROM USERS").fetchall()
    return render_template("list.jinja", items=users, headers=headers, type="user", admin=True)


@admin.route("/golinks")
@auth.requires_auth(["admin"])
def golink_list(user, userinfo):
    headers = db.get_db().execute("PRAGMA table_info(golinks)").fetchall()
    golinks = db.get_db().execute("SELECT * FROM golinks").fetchall()
    return render_template("list.jinja", items=golinks, headers=headers, type="golink", admin=True)


@admin.route("/infoboxes")
@auth.requires_auth(["manage_own_infoboxes"])
def infobox_manage(user, userinfo):
    headers = db.get_db().execute("PRAGMA table_info(infoboxes)").fetchall()
    if auth.has_permission(user, "admin"):
        infoboxes = (
            db.get_db()
            .execute("SELECT * FROM infoboxes ORDER BY type, displayorder")
            .fetchall()
        )
        admin = True
    else:
        infoboxes = (
            db.get_db()
            .execute("SELECT * FROM infoboxes WHERE owner = ? ORDER BY type, displayorder", (user["id"],))
            .fetchall()
        )
        admin = False
    return render_template(
        "list.jinja", items=infoboxes, headers=headers, type="infoboxes", admin=admin
    )


@admin.route("/infoboxes/create")
@auth.requires_auth(["admin"])
def infobox_create(user, userinfo):
    return render_template("infobox_create.jinja")


@admin.route("/infoboxes/create/submit", methods=["post"])
@auth.requires_auth(["admin"])
def infobox_create_submit(user, userinfo):
    print(request.form["description"])
    description = request.form["description"].replace("\n", "<br>")
    database = db.get_db()
    database.execute(
        "INSERT INTO infoboxes (name, type, description, categoryid, owner, displayorder) VALUES (?, ?, ?, ?, ?, ?);",
        (
            request.form["name"],
            request.form["type"],
            description,
            request.form["categoryid"],
            request.form["owner"],
            request.form["displayorder"],
        ),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/links")
@auth.requires_auth(["admin"])
def links_list(user, userinfo):
    headers = db.get_db().execute("PRAGMA table_info(links)").fetchall()
    infoboxes = db.get_db().execute("SELECT * FROM links").fetchall()
    return render_template("list.jinja", items=infoboxes, headers=headers, type="links", admin=True)


@admin.route("/categories")
@auth.requires_auth(["admin"])
def categories_manage(user, userinfo):
    headers = db.get_db().execute("PRAGMA table_info(categories)").fetchall()
    infoboxes = (
        db.get_db()
        .execute("SELECT * FROM categories ORDER BY type, displayorder")
        .fetchall()
    )
    return render_template(
        "list.jinja", items=infoboxes, headers=headers, type="categories", admin=True
    )


@admin.route("/categories/create")
@auth.requires_auth(["admin"])
def category_create(user, userinfo):
    return render_template("category_create.jinja")


@admin.route("/categories/create/submit", methods=["post"])
@auth.requires_auth(["admin"])
def category_create_submit(user, userinfo):
    database = db.get_db()
    database.execute(
        "INSERT INTO categories (name, displayorder, type) VALUES (?, ?, ?);",
        (request.form["name"], request.form["displayorder"], request.form["type"]),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/infoboxes/<int:id>/edit")
@auth.requires_auth(["manage_own_infoboxes"])
def infobox_edit(user, userinfo, id):
    links = db.get_db().execute("SELECT * FROM links WHERE infoboxid = ?", (id,))
    infobox = (
        db.get_db().execute("SELECT * FROM infoboxes WHERE id = ?", (id,)).fetchone()
    )
    description = infobox["description"].replace("<br>", "\n")
    if auth.has_permission(user, "admin") or infobox["owner"] == user["id"]:
        return render_template("infobox_edit.jinja", infobox=infobox, description=description, links=links,
                               admin=auth.has_permission(user, "admin"))
    else:
        abort(403)


@admin.route("/categories/<int:id>/edit")
@auth.requires_auth(["admin"])
def category_edit(user, userinfo, id):
    category = (
        db.get_db().execute("SELECT * FROM categories WHERE id = ?", (id,)).fetchall()
    )
    return render_template("category_edit.jinja", category=category)


@admin.route("/categories/<int:id>/delete")
@auth.requires_auth(["admin"])
def category_delete(user, userinfo, id):
    database = db.get_db()
    database.execute("DELETE FROM categories WHERE id = ?", (id,))
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/infoboxes/<int:id>/delete")
@auth.requires_auth(["admin"])
def infobox_delete(user, userinfo, id):
    database = db.get_db()
    database.execute("DELETE FROM infoboxes WHERE id = ?", (id,))
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/categories/<int:id>/edit/submit", methods=["post"])
@auth.requires_auth(["admin"])
def category_edit_submit(user, userinfo, id):
    database = db.get_db()
    database.execute(
        "UPDATE categories SET name = ?, type = ?, displayorder = ? WHERE id = ?;",
        (request.form["name"], request.form["type"], request.form["displayorder"], id),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/infoboxes/<int:id>/edit/submit", methods=["post"])
@auth.requires_auth(["manage_own_infoboxes"])
def infobox_edit_submit(user, userinfo, id):
    database = db.get_db()
    if auth.has_permission(user, "admin"):
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
    else:
        infobox = (
            database.execute("SELECT owner FROM infoboxes WHERE id = ?", (id,)).fetchall()
        )
        if infobox[0]["owner"] == user["id"]:
            database.execute(
                "UPDATE infoboxes SET name = ?, description = ? WHERE id = ?;",
                (
                    request.form["name"],
                    request.form["description"],
                    id
                ),
            )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/links/<int:id>/edit/submit", methods=["post"])
@auth.requires_auth(["manage_own_infoboxes"])
def link_edit_submit(user, userinfo, id):
    database = db.get_db()
    infoboxid = database.execute("SELECT infoboxid from links WHERE id = ?", (id,)).fetchall()[0][0]
    infoboxOwner = database.execute("SELECT owner from infoboxes WHERE id = ?", (infoboxid,)).fetchall()[0][0]
    if auth.has_permission(user, "admin") or user["id"] == infoboxOwner:
        database.execute(
            "UPDATE links SET name = ?, destination = ? WHERE id = ?;",
            (request.form["name"], request.form["destination"], id),
        )
    else:
        abort(403)
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/links/<int:id>/delete")
@auth.requires_auth(["manage_own_infoboxes"])
def link_delete(user, userinfo, id):
    database = db.get_db()
    infoboxid = database.execute("SELECT infoboxid from links WHERE id = ?", (id,)).fetchall()[0][0]
    infoboxOwner = database.execute("SELECT owner from infoboxes WHERE id = ?", (infoboxid,)).fetchall()[0][0]
    if auth.has_permission(user, "admin") or user["id"] == infoboxOwner:
        database.execute(
            "DELETE FROM links WHERE id = ?;",
            (id,),
        )
    else:
        abort(403)
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/links/create/submit", methods=["post"])
@auth.requires_auth(["manage_own_infoboxes"])
def link_create_submit(user, userinfo):
    infoboxid = None
    if request.form.get("infoboxid", None):
        infoboxid = request.form["infoboxid"]
    elif request.args.get("infoboxid", None):
        infoboxid = request.args["infoboxid"]
    else:
        abort(400)
    database = db.get_db()
    infoboxOwner = database.execute("SELECT owner from infoboxes WHERE id = ?", (infoboxid,)).fetchall()[0][0]
    if auth.has_permission(user, "admin") or user["id"] == infoboxOwner:
        database.execute(
            "INSERT INTO links (name, destination, infoboxid) VALUES (?, ?, ?)",
            (request.form["name"], request.form["destination"], infoboxid),
        )
        database.commit()
    else:
        abort(403)
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/announcements")
@auth.requires_auth(["admin"])
def announcements(user, userinfo):
    headers = db.get_db().execute("PRAGMA table_info(announcements)").fetchall()
    announcements = (
        db.get_db()
        .execute("SELECT * FROM announcements")
        .fetchall()
    )
    admin = True
    return render_template(
        "list.jinja", items=announcements, headers=headers, type="announcements", admin=admin
    )


@admin.route("/announcements/create")
@auth.requires_auth(["admin"])
def announcement_create(user, userinfo):
    return render_template("announcement_create.jinja")


@admin.route("/announcements/create/submit", methods=["post"])
@auth.requires_auth(["admin"])
def announcement_create_submit(user, userinfo):
    database = db.get_db()
    if request.form.get("enabled", None):
        enabled = True
    else:
        enabled = False
    database.execute(
        "INSERT INTO announcements (text, enabled) VALUES (?, ?);",
        (request.form["text"], enabled),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/announcements/<int:id>/edit")
@auth.requires_auth(["admin"])
def announcement_edit(user, userinfo, id):
    announcement = (
        db.get_db().execute("SELECT * FROM announcements WHERE id = ?", (id,)).fetchone()
    )
    return render_template("announcement_edit.jinja", announcement=announcement)


@admin.route("/announcements/<int:id>/edit/submit", methods=["post"])
@auth.requires_auth(["admin"])
def announcement_edit_submit(user, userinfo, id):
    if request.form.get("enabled", None):
        enabled = True
    else:
        enabled = False
    database = db.get_db()
    database.execute(
        "UPDATE announcements SET text = ?, enabled = ? WHERE id = ?;",
        (request.form["text"], enabled, id),
    )
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)


@admin.route("/announcements/<int:id>/delete")
@auth.requires_auth(["admin"])
def announcement_delete(user, userinfo, id):
    database = db.get_db()
    database.execute("DELETE FROM announcements WHERE id = ?", (id,))
    database.commit()
    flash("Done!", "success")
    return redirect(request.referrer)
