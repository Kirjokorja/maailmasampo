import sqlite3
import secrets
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session

import db
import config
import users
import projects
import items

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: virheellinen tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register_user.html")

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    password_confirm = request.form["password_confirm"]
    if password != password_confirm:
        flash("VIRHE: salasanat eivät täsmää")
        return redirect("/register")
    try:
        users.create_user(username, password)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")
    flash("Tunnus luotu")
    return redirect("/")

@app.route("/user/<int:user_id>")
def show_user(user_id):
    require_login()
    user = users.get_user(user_id)
    if not user:
        abort(404)
    return render_template("show_user.html", user=user)

@app.route("/users")
def all_users():
    require_login()
    results = users.get_all_users()
    return render_template("users.html", results=results)

@app.route("/find_user")
def find_user():
    require_login()
    query = request.args.get("query")
    if query:
        results = users.find_users(query)
    else:
        query = ""
        results = []
    return render_template("find_user.html", query=query, results=results)

@app.route("/new_project")
def new_project():
    require_login()
    return render_template("new_project.html")

@app.route("/create_project", methods=["POST"])
def create_project():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    projects.add_project(title, description)
    project_id = db.last_insert_id()
    return redirect("/project/" + str(project_id))

@app.route("/project/<int:project_id>")
def show_project(project_id):
    require_login()
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    return render_template("show_project.html", project=project)

@app.route("/find_project")
def find_project():
    require_login()
    query = request.args.get("query")
    if query:
        results = projects.find_projects(query)
    else:
        query = ""
        results = []
    return render_template("find_project.html", query=query, results=results)

@app.route("/edit_project/<int:project_id>")
def edit_project(project_id):
    require_login()
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    return render_template("edit_project.html", project=project)


@app.route("/update_project", methods=["POST"])
def update_project():
    require_login()
    check_csrf()

    project_id = request.form["project_id"]
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    projects.update_project(project_id, title, description)
    return redirect("/project/" + str(project_id))

@app.route("/remove_project/<int:project_id>", methods=["GET", "POST"])
def remove_project(project_id):
    require_login()
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    if request.method == "GET":
        return render_template("remove_project.html", project=project)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            projects.remove_project(project_id)
            return redirect("/")
        else:
            return redirect("/project/" + str(project_id))

@app.route("/new_item")
def new_item():
    require_login()
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    items.add_item(title, description)
    item_id = db.last_insert_id()
    return redirect("/item/" + str(item_id))

@app.route("/find_item")
def find_item():
    require_login()
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("edit_item.html", item=item)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    items.update_item(item_id, title, description)
    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if request.method == "GET":
        return render_template("remove_item.html", item=item)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))
