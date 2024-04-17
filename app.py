import dotenv
from flask import Flask, render_template, request
import os

import werkzeug
from scratch import scratch
from main import main
from util import util


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

# allow loading all assets from all subdomains
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = f"*"
    return response

@app.context_processor
def inject_english_mode():
    return {"english": bool(request.cookies.get("english", False))}

@app.context_processor
def inject_server_name():
    return {"server_name": os.environ.get("SERVER_NAME")}

app.register_blueprint(main)
app.register_blueprint(scratch)
app.register_blueprint(util)


# default error handler
@app.errorhandler(werkzeug.exceptions.HTTPException)
def error(error: werkzeug.exceptions.HTTPException):
  return render_template("error.jinja", error=error)

if __name__ == "__main__":
    app.run("0.0.0.0", "9000", debug=True)
