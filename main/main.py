import json
import os
import requests
from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    Response,
    url_for,
)

import auth
import db

endpoint_stats = {}

main = Blueprint("main", __name__, template_folder="templates", url_prefix="")


@main.before_request
def log_request():
    if endpoint_stats.get(request.endpoint, None) is None:
        endpoint_stats[request.endpoint] = 1
    else:
        endpoint_stats[request.endpoint] += 1


@main.route("/")
def index():
    return render_template("index.jinja")


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@main.route("/sitemap.xml")
def sitemap():
    links = []
    for rule in current_app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            # ignore some endpoints
            if not (
                    url.startswith("/login")
                    | url.startswith("/admin")
                    | url.startswith("/go")
                    | url.startswith("/util")
                    | url.endswith("-sub")
            ):
                links.append(request.url_root[0:-1] + url)  # slice: remove ending /
    # add missing URLs
    links.append(request.url_root[0:-1] + "/scratch/practice/letter")
    links.append(request.url_root[0:-1] + "/scratch/practice/word")
    return Response(
        render_template("sitemap.xml.jinja", urls=links), mimetype="application/xml"
    )


@main.route("/robots.txt")
def robots():
    return Response(
        render_template("robots.txt.jinja", url_base=request.root_url), mimetype="plain"
    )


@main.route("/stats")
def stats():
    resp = Response(
        json.dumps(endpoint_stats, sort_keys=True), mimetype="application/json"
    )
    return resp


@main.route("/about")
def about():
    return render_template("about.jinja")


@main.route("/community")
def community():
    return render_template("community.jinja")


@main.route("/groups")
def community_groups():
    database = db.get_db()
    groups = database.execute(
        "SELECT * FROM infoboxes WHERE type = 'group' ORDER BY displayorder"
    ).fetchall()
    categories = database.execute(
        "SELECT * FROM categories WHERE type = 'group' ORDER BY displayorder"
    ).fetchall()
    links = database.execute("SELECT * FROM links").fetchall()
    print(groups)
    return render_template(
        "groups.jinja", groups=groups, links=links, categories=categories
    )


@main.route("/content")
def community_content():
    database = db.get_db()
    content = database.execute(
        "SELECT * FROM infoboxes WHERE type = 'content' ORDER BY displayorder"
    ).fetchall()
    categories = database.execute(
        "SELECT * FROM categories WHERE type = 'content' ORDER BY displayorder"
    ).fetchall()
    links = database.execute("SELECT * FROM links").fetchall()
    return render_template(
        "content.jinja", groups=content, links=links, categories=categories
    )


@main.route("/contact", methods=["GET", "POST"])
def _contact():
    if request.method == "GET":
        return render_template("contact.jinja")
    else:
        # it's a POST request! Send it to our discord webhook
        requests.post(
            os.environ.get("MESSENGER_WEBHOOK_URL"),
            json={
                "username": "avali.zone messenger",
                "avatar_url": f"{request.url_root}/static/icons/avali.png",
                "content": f"<@{os.environ.get('OWNER_USER_ID')}>",
                "embeds": [
                    {
                        "author": {"name": request.form.get("name")},
                        "title": f"New {request.form.get('reason')}",
                        "description": request.form.get("message"),
                        "fields": [
                            {
                                "name": "Contact",
                                "value": request.form.get("contact"),
                                "inline": True,
                            },
                        ],
                    }
                ],
            },
        )
        # Done! Now let's give the user a nice page
        return render_template("contact_success.jinja")


@main.route("/lore/wiki")
def wiki():
    return render_template("lore/wiki.jinja")


@main.route("/lore/book")
def book():
    return render_template("lore/book.jinja")


@main.route("/panel")
@auth.requires_auth([])
def panel(userinfo, user):
    permissions = {}

    if auth.has_permission(user, "golink_approved"):
        permissions["golinks"] = "/go"

    if auth.has_permission(user, "manage_own_infoboxes"):
        permissions["Manage infoboxes"] = "/admin/infoboxes"

    if auth.has_permission(user, "admin"):
        permissions["User list"] = "/admin/users"
        permissions["Manage (infobox) Categories"] = "/admin/categories"
        permissions["(Infobox) Link List"] = "/admin/links"
        permissions["Golink list"] = "/admin/golinks"
        permissions["Manage Announcements"] = "/admin/announcements"

    return render_template("panel.jinja", permissions=permissions, userinfo=userinfo)


@main.route("/lore")
def lore():
    return render_template("lore.jinja")
