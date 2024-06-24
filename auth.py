from flask import abort, render_template
from flask_dance.contrib.google import google
import db


def requires_auth(requirements: list[str]):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not google.authorized:
                return render_template("login_required.jinja")

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
                    
            return f(*args, **kwargs, userinfo=userinfo, user=user)

        wrapper.__name__ = f.__name__
        return wrapper

    return decorator


def has_permission(user, name):
    if user["admin"]:
        return True
    return user[name]
