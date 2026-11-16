"""
Facebook — mockup activity project (login-only version, MySQL-backed)
--------------------------------------------------------------------------
Log In and Sign Up are now SEPARATE PAGES:
  - "/"        -> login.html  (the log in form, or the welcome card if logged in)
  - "/signup"  -> signup.html (the create-account form)
"Create new account" on the login page is a plain link to /signup; "Log in
instead" on the signup page is a plain link back to /.

User accounts live in a real MySQL database (via XAMPP) through db.py.

FIRST-TIME SETUP (only once):
    1. Start MySQL (and Apache) in the XAMPP Control Panel.
    2. pip install -r requirements.txt
    3. python init_db.py        <-- creates the database/table + demo account

THEN, EVERY TIME YOU WANT TO RUN IT:
    4. python app.py
    5. Open http://127.0.0.1:5000 in your browser.

Do NOT double-click login.html/signup.html or open them with a file:// URL —
the {% ... %} / {{ ... }} template tags only get filled in when Flask serves
the page through render_template().
"""

import re
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session

import db

# NOTE: passwords are stored and compared in PLAIN TEXT (no hashing) by
# request, so they show up readable in phpMyAdmin. Fine for this local
# school mockup — never do this in a real app with real users.

app = Flask(__name__, template_folder=".", static_folder=".", static_url_path="")
app.secret_key = "mockup-activity-secret-key"  # fine for a local practice demo only

# ----- Identifier validation (email or phone) -----
EMAIL_RE = re.compile(r"^[\w.+-]+@(gmail|yahoo)\.com$", re.IGNORECASE)

# Valid PH mobile number shapes only (not just "any 7-15 digits"):
#   09XXXXXXXXX      (11 digits, local format, e.g. 09171234567)
#   +639XXXXXXXXX    (country code + 9-digit subscriber number)
PH_PHONE_RE = re.compile(r"^(09\d{9}|\+639\d{9})$")


def is_allowed_email(value: str) -> bool:
    """Gmail/Yahoo only — used for the Sign Up page's email field."""
    return bool(EMAIL_RE.match(value))


def is_allowed_identifier(value: str) -> bool:
    """Gmail/Yahoo email OR a valid PH mobile number — used for the Log In field."""
    if is_allowed_email(value):
        return True
    digits_and_plus_only = value.replace(" ", "").replace("-", "")
    return bool(PH_PHONE_RE.match(digits_and_plus_only))


IDENTIFIER_HINT = (
    "The email or mobile number you entered isn't connected to an account. "
)
EMAIL_HINT = "Please use a Gmail or Yahoo email address."
DB_DOWN_HINT = (
    "Couldn't reach the database. In XAMPP's Control Panel, make sure "
    "MySQL is started, then try again."
)


@app.route("/")
def index():
    """The Log In page, or the welcome card if already logged in."""
    user_name = session.get("user_name")
    return render_template("login.html", logged_in=bool(user_name), user_name=user_name)


@app.route("/login", methods=["POST"])
def login():
    identifier = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = None
    error_field = None       # which input gets the red border: "email", "password", or None
    show_account_link = False  # whether to show the "Create a new account" action link

    if not identifier or not password:
        error = "Please fill in both fields."
    elif not is_allowed_identifier(identifier):
        error = IDENTIFIER_HINT
        error_field = "email"
        show_account_link = True
    else:
        try:
            user = db.find_user_by_identifier(identifier)
        except mysql.connector.Error:
            error = DB_DOWN_HINT
        else:
            if user is not None:
                # This identifier already has a real account in the database
                # (e.g. the seeded demo account, or anyone who signed up/
                # logged in before) — its real password still has to match.
                if user["password"] != password:
                    error = "Incorrect password for this account."
                    error_field = "password"
                else:
                    session["user_email"] = user["identifier"]
                    session["user_name"] = user["name"]
                    return redirect(url_for("index"))
            else:
                # Mockup rule: no account on file yet, but the identifier is
                # a valid Gmail/Yahoo/PH-number format — create a real row
                # for it right now (so it DOES show up in the database),
                # then log them straight in.
                guest_name = (
                    identifier.split("@")[0].title() if "@" in identifier else "Guest"
                )
                try:
                    db.create_user(guest_name, identifier, password)
                except mysql.connector.Error:
                    error = DB_DOWN_HINT
                else:
                    session["user_email"] = identifier
                    session["user_name"] = guest_name
                    return redirect(url_for("index"))

    return render_template(
        "login.html",
        error=error,
        error_field=error_field,
        show_account_link=show_account_link,
        prefill_email=identifier,
    )


@app.route("/signup", methods=["GET"])
def signup_page():
    """The Create Account page itself (separate from the POST that submits it)."""
    if session.get("user_name"):
        return redirect(url_for("index"))
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    error = None
    if not name or not email or not password:
        error = "Please fill in your name, email, and password."
    elif not is_allowed_email(email):
        error = EMAIL_HINT
    else:
        try:
            if db.find_user_by_identifier(email) is not None:
                error = "An account with that email already exists (try logging in)."
            else:
                db.create_user(name, email, password)
                session["user_email"] = email
                session["user_name"] = name
                return redirect(url_for("index"))
        except mysql.connector.Error:
            error = DB_DOWN_HINT

    return render_template("signup.html", error=error, prefill_name=name, prefill_email=email)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
