from flask import Flask, render_template, request, redirect, Response
import json
import requests
import werkzeug
import dotenv
import os
import werkzeug.exceptions

from blueprints.scratch import scratch

endpoint_stats = {}

dotenv.load_dotenv()
app = Flask(__name__, subdomain_matching=True, static_folder=None)
app.config["SERVER_NAME"] = os.environ.get("SERVER_NAME")
app.static_folder = "static"
app.add_url_rule(
    "/<path:filename>",
    subdomain="static",
    endpoint="static",
    view_func=app.send_static_file,
)

app.register_blueprint(scratch, subdomain="scratch")


@app.context_processor
def inject_english_mode():
    return {"english": bool(request.cookies.get("english", False))}


@app.context_processor
def inject_server_name():
    return {"server_name": os.environ.get("SERVER_NAME")}


@app.before_request
def log_request():
    if endpoint_stats.get(request.endpoint, None) is None:
        endpoint_stats[request.endpoint] = 1
    else:
        endpoint_stats[request.endpoint] += 1


# allow loading all assets from all subdomains
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = f"*"
    return response


@app.route("/")
def index():
    return render_template("index.jinja")


@app.route("/stats")
def stats():
    resp = Response(
        json.dumps(endpoint_stats, sort_keys=True), mimetype="application/json"
    )
    return resp


@app.route("/about")
def about():
    return render_template("about.jinja")


@app.route("/community")
def community():
    return render_template("community.jinja")


@app.route("/groups")
def community_groups():
    return render_template("groups.jinja")


@app.route("/content")
def community_content():
    return render_template("content.jinja")


@app.route("/contact", methods=["GET", "POST"])
def contact():
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


@app.route("/util/togglelang")
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


@app.route("/lore/wiki")
def wiki():
    return render_template("lore/wiki.jinja")


@app.route("/lore/book")
def book():
    return render_template("lore/book.jinja")


@app.route("/lore")
def lore():
    return render_template("lore.jinja")


@app.errorhandler(werkzeug.exceptions.HTTPException)
def error(error: werkzeug.exceptions.HTTPException):
    server_url = f"{request.scheme}://{os.getenv('SERVER_NAME')}"
    scratch_url = f"{request.scheme}://scratch.{os.getenv('SERVER_NAME')}"

    if request.host_url.rstrip("/") == server_url:
        # throw main error page for main site
        return render_template("error.jinja", error=error), error.code
    elif request.host_url.rstrip("/") == scratch_url:
        return render_template("scratch/error.jinja", error=error), error.code
    else:
        # if the request is for a different subdomain, and it is invalid, redirect to the main site
        return redirect(f"{server_url}")


if __name__ == "__main__":
    app.run("0.0.0.0", "9000", debug=True)
