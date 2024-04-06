from flask import Blueprint, Flask, render_template, request, redirect
import werkzeug
import dotenv
import os
import werkzeug.exceptions

from blueprints.scratch import scratch

dotenv.load_dotenv()
app = Flask(__name__, subdomain_matching=True, static_folder=None)
app.config['SERVER_NAME'] = os.environ.get("SERVER_NAME")
app.static_folder = 'static'
app.add_url_rule('/<path:filename>',
                 subdomain="static",
                 endpoint='/',
                 view_func=app.send_static_file)

app.register_blueprint(scratch, subdomain="scratch")

@app.context_processor
def inject_english_mode():
    return {"english": bool(request.cookies.get("english", False))}

@app.context_processor
def inject_server_name():
    return {"server_name": os.environ.get("SERVER_NAME")}

# allow loading all assets from all subdomains
@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = f"*"
    return response

@app.route("/")
def hello_world():
    return render_template("index.jinja")
    
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

@app.route("/util/togglelang")
def togglelang():
    resp = redirect(request.referrer)
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