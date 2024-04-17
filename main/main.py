import os
from flask import Blueprint, render_template, request, redirect, Response
import json
import requests
import werkzeug.exceptions

endpoint_stats = {}

main = Blueprint("main", __name__, template_folder="templates", subdomain="")


@main.before_request
def log_request():
    if endpoint_stats.get(request.endpoint, None) is None:
        endpoint_stats[request.endpoint] = 1
    else:
        endpoint_stats[request.endpoint] += 1


@main.route("/")
def index():
    return render_template("index.jinja")


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
    return render_template("groups.jinja")


@main.route("/content")
def community_content():
    return render_template("content.jinja")

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
                "avatar_url": f"https://static.{os.environ.get('SERVER_NAME')}/icons/avali.png",
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


@main.route("/lore")
def lore():
    return render_template("lore.jinja")

