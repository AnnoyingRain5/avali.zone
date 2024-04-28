from flask import redirect, url_for, abort
from flask_dance.contrib.google import google
import db

def requires_auth(requirements: list[str]):
    def decorator(f):
        def wrapper(*args, **kwargs):
            if not google.authorized:
                return redirect(url_for("google.login"))
            
            userinfo = google.get('/oauth2/v1/userinfo').json()
            database = db.get_db()
            user = database.execute("SELECT * FROM users WHERE id = ?", (f"GOOGLE_{userinfo['id']}",)).fetchone()
            if not user:
                # user is not in db
                user = database.execute("INSERT INTO users VALUES (?, false, false)", (f"GOOGLE_{userinfo['id']}",)).fetchone()
                database.commit()
                if requirements:
                    abort(403)

            # admins pass all checks automatically
            if user["ADMIN"]:
                return f(*args, **kwargs, userinfo=userinfo, user=user)
            
            for requirement in requirements:
                match requirement:
                    case "golink":
                        if not user["golink_approved"]:
                            abort(403)
            return f(*args, **kwargs, userinfo=userinfo, user=user)
        return wrapper
    return decorator

def has_permission(user, name):
    if user["admin"]:
        return True
    return user[name]