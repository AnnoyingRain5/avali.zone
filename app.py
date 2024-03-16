from flask import Flask, render_template, request, redirect
import werkzeug
import werkzeug.exceptions

app = Flask(__name__)


@app.context_processor
def inject_english_mode():
    return {"english": bool(request.cookies.get("english", False))}


@app.route("/")
def hello_world():
    return render_template("index.jinja")
    
@app.route("/about")
def about():
    return render_template("about.jinja")

@app.route("/community")
def community():
    return render_template("community.jinja")

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
def error_404(error: werkzeug.exceptions.HTTPException):
    return render_template("error.jinja", error=error)

if __name__ == "__main__":
    app.run("0.0.0.0", "9000", debug=True)