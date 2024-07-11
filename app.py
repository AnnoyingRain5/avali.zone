import dotenv
from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_dance.contrib.google import make_google_blueprint
import os
import werkzeug
from flask_compress import Compress

from scratch import scratch
from main import main
from util import util
from go import go
from admin import admin

import db
import upgrade_db


upgrade_db.upgrade_if_needed()
dotenv.load_dotenv()
app = Flask(__name__, subdomain_matching=True)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 3600  # one hour
app.wsgi_app = ProxyFix(app.wsgi_app)
db.init_app(app)
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
# id, name, given_name, picture (which is a url to the profile picture) and locale
googleprint = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    offline=True,
    redirect_url="/panel",
    reprompt_consent=True,
    scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
)

app.register_blueprint(main)
app.register_blueprint(scratch)
app.register_blueprint(util)
app.register_blueprint(go)
app.register_blueprint(admin)
app.register_blueprint(googleprint, url_prefix="/login")


# default error handler
@app.errorhandler(werkzeug.exceptions.HTTPException)
def error(error: werkzeug.exceptions.HTTPException):
    return render_template("error.jinja", error=error)


if __name__ == "__main__":
    app.run("0.0.0.0", "9000", debug=True)
