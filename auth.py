import os
from flask import abort, render_template
from flask_dance import OAuth2ConsumerBlueprint
from flask_dance.contrib.google import google, make_google_blueprint
import db

googleprint = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    offline=True,
    redirect_url="/panel",
    reprompt_consent=True,
    scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
)
print(os.environ.get("POCKETID_CLIENT_ID"))
print(os.environ.get("POCKETID_CLIENT_ID"))
pocketid = OAuth2ConsumerBlueprint(
    "avali", __name__,
    client_id=os.environ.get("POCKETID_CLIENT_ID"),
    client_secret=os.environ.get("POCKETID_CLIENT_SECRET"),
    base_url="https://auth.avali.zone",
    token_url="https://auth.avali.zone/api/oidc/token",
    authorization_url="https://auth.avali.zone/authorize",
    scope=["openid", "email", "profile"],
    redirect_url="/panel",
)


def requires_auth(requirements: list[str]):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if google.authorized:
                userinfo = google.get("/oauth2/v3/userinfo").json()
                database = db.get_db()
                user = database.execute(
                    "SELECT * FROM users WHERE id = ?", (f"GOOGLE_{userinfo['email']}",)
                ).fetchone()
                if not user:
                    # user is not in db
                    database.execute(
                        "INSERT INTO users VALUES (?, false, false, false)",
                        (f"GOOGLE_{userinfo['email']}",),
                    )
                    user = database.execute(
                        "SELECT * FROM users WHERE id = ?", (f"GOOGLE_{userinfo['email']}",)
                    ).fetchone()
                    database.commit()
                    if requirements:
                        abort(403)
                for requirement in requirements:
                    if not has_permission(user, requirement):
                        abort(403)
            elif pocketid.session.authorized:
                userinfo = pocketid.session.get("https://auth.avali.zone/api/oidc/userinfo").json()
                database = db.get_db()
                user = database.execute(
                    "SELECT * FROM users WHERE id = ?", (f"POCKETID_{userinfo['email']}",)
                ).fetchone()
                if not user:
                    # user is not in db
                    database.execute(
                        "INSERT INTO users VALUES (?, false, false, false)",
                        (f"POCKETID_{userinfo['email']}",),
                    )
                    user = database.execute(
                        "SELECT * FROM users WHERE id = ?", (f"POCKETID_{userinfo['email']}",)
                    ).fetchone()
                    database.commit()
                    if requirements:
                        abort(403)
                for requirement in requirements:
                    if not has_permission(user, requirement):
                        abort(403)
            else:
                return render_template("login_required.jinja")
            return f(*args, **kwargs, userinfo=userinfo, user=user)

        wrapper.__name__ = f.__name__
        return wrapper

    return decorator


def has_permission(user, name):
    if user["admin"]:
        return True
    return user[name]
