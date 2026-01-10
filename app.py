import dotenv
dotenv.load_dotenv()
import os
import werkzeug
from flask import Flask, render_template, request, redirect
from flask_compress import Compress
from werkzeug.middleware.proxy_fix import ProxyFix

import auth
import db
import upgrade_db
from admin import admin
from go import go
from main import main
from scratch import scratch
from util import util

app = Flask(__name__, subdomain_matching=True)
db.init_app(app)
upgrade_db.upgrade_if_needed()
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600  # one hour
app.wsgi_app = ProxyFix(app.wsgi_app)
Compress(app)


# allow loading all assets from all subdomains
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = f"*"
    return response


@app.context_processor
def inject_english_mode():
    return {"fontchoice": request.cookies.get("fontchoice", None)}


@app.context_processor
def inject_announcements():
    return {"announcements": db.get_db().execute("SELECT * FROM announcements WHERE enabled").fetchall()}


@app.context_processor
def inject_environment():
    return {"environment": os.environ.get("ENVIRONMENT_TYPE", "production")}


# this uses the userinfo.profile scope, which provides:
# id, name, given_name, picture (which is a URL to the profile picture) and locale

app.register_blueprint(main)
app.register_blueprint(scratch)
app.register_blueprint(util)
app.register_blueprint(go)
app.register_blueprint(admin)

app.register_blueprint(auth.pocketid, url_prefix="/login")
app.register_blueprint(auth.googleprint, url_prefix="/login")

@app.route("/.well-known/host-meta")
def well_known_host_meta():
    return redirect("https://social.avali.zone/.well-known/host-meta")
@app.route("/.well-known/webfinger")
def well_known_webfinger():
    return redirect(f"https://social.avali.zone/.well-known/webfinger?{request.query_string.decode()}")

# default error handler
@app.errorhandler(werkzeug.exceptions.HTTPException)
def error(exception: werkzeug.exceptions.HTTPException):
    return render_template("error.jinja", error=exception)


if __name__ == "__main__":
    app.run("0.0.0.0", 9000, debug=True)
