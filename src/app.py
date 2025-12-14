import secrets
import math
import time
from flask import Flask
from flask import abort, flash, redirect, render_template, request, session, g

import config
import classes
import users
import projects
import items
import exceptions

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def check_csrf():
    if "csrf_token" not in request.form or request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

def require_login():
    if "user_id" not in session:
        abort(403)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_id = users.check_login(username, password)
        if user_id:
            action_id = classes.get_class_id('Käyttäjätoiminto', 'sisäänkirjautuminen')
            users.log_user(user_id, action_id)
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        flash("VIRHE: virheellinen tunnus tai salasana")
        return redirect("/")
    return render_template("index.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        user_id = session["user_id"]
        del session["user_id"]
        del session["username"]
        action_id = classes.get_class_id('Käyttäjätoiminto', 'uloskirjautuminen')
        users.log_user(user_id, action_id)
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register_user.html")

@app.route("/create-user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password = request.form["password"]
    password_confirm = request.form["password_confirm"]
    if password != password_confirm:
        flash("VIRHE: salasanat eivät täsmää")
        return redirect("/register")
    try:
        users.create_user(username, password)
    except exceptions.UserAlreadyExists:
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
    require_login()
    page_size = 10
    page_count = 0
    page = 1

    if request.args.get("page"):
        page = int(request.args.get("page"))

    user_items_count = users.count_user_items(user_id)
    page_count = math.ceil(user_items_count/page_size)
    page_count = max(page_count, 1)
    page = max(page, 1)
    page = min(page, page_count)
    user_items = users.get_user_items(user_id, page, page_size)

    return render_template("show_user.html", page=page, page_count=page_count,
                           user=user, user_items_count=user_items_count, user_items=user_items)

@app.route("/find-user")
def find_user():
    require_login()

    page_size = 10
    page_count = 0
    results = []
    query = ""
    page = 1

    if request.args.get("page"):
        page = int(request.args.get("page"))

    if request.args.get("query"):
        query = request.args.get("query")
        results_count = users.count_users(query)
        page_count = math.ceil(results_count/page_size)
        page_count = max(page_count, 1)
        page = max(page, 1)
        page = min(page, page_count)
        results = users.find_users(query, page, page_size)

    return render_template("find_user.html", page=page, page_count=page_count,
                           query=query, results=results)

@app.route("/new-project")
def new_project():
    require_login()
    all_classes = classes.get_all_classes('Hanke')
    return render_template("new_project.html", all_classes=all_classes)

@app.route("/create-project", methods=["POST"])
def create_project():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(400)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(400)

    class_id = int(request.form["class"])
    all_classes = classes.get_all_classes('Hanke').keys()
    if class_id not in all_classes:
        abort(400)
    project_id = projects.add_project(title, description, session["user_id"], class_id)
    if not project_id:
        flash("VIRHE: hanketta ei voitu luoda")
        return redirect("/new-project")
    return redirect("/project/" + str(project_id))

@app.route("/project/<int:project_id>")
def show_project(project_id):
    require_login()
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    return render_template("show_project.html", project=project)

@app.route("/find-project")
def find_projects():
    require_login()
    query = request.args.get("query")
    results = []
    if query:
        results = projects.find_projects(query)
    else:
        query = ""
    return render_template("find_project.html", query=query, results=results)

@app.route("/edit-project/<int:project_id>")
def edit_project(project_id):
    require_login()
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    return render_template("edit_project.html", project=project)


@app.route("/update-project", methods=["POST"])
def update_project():
    require_login()
    check_csrf()

    project_id = request.form["project_id"]
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(400)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(400)
    projects.update_project(project_id, title, description)
    return redirect("/project/" + str(project_id))

@app.route("/remove-project/<int:project_id>", methods=["GET", "POST"])
def remove_project(project_id):
    require_login()
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            projects.remove_project(project_id)
            return redirect("/")
        return redirect("/project/" + str(project_id))
    return render_template("remove_project.html", project=project)

@app.route("/find-projects-items")
def find_projects_items():
    require_login()
    page_size = 10
    page_count = 0
    results = []
    query = ""
    page = 1

    if request.args.get("page"):
        page = int(request.args.get("page"))

    if request.args.get("query"):
        query = request.args.get("query")
        results_count = projects.count_projects_items(query)
        page_count = math.ceil(results_count/page_size)
        page_count = max(page_count, 1)
        page = max(page, 1)
        page = min(page, page_count)
        results = projects.find_projects_items(query, page, page_size)

    return render_template("find_projects_items.html", page=page, page_count=page_count,
                           query=query, results=results)

@app.route("/project/<int:project_id>/new-item")
def new_item(project_id):
    require_login()
    project = projects.get_project(project_id)
    if not project:
        abort(404)
    all_classes = classes.get_all_classes('Luokka')
    return render_template("new_item.html", project=project, all_classes=all_classes)

@app.route("/create-item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()

    project_id = request.form["project_id"]
    if not project_id:
        abort(400)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(400)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(400)

    class_id = int(request.form["class"])
    all_classes = classes.get_all_classes('Luokka').keys()
    if class_id not in all_classes:
        abort(400)
    item_id = items.add_item(title, description, session["user_id"], class_id, project_id)
    if not item_id:
        flash("VIRHE: kohdetta ei voitu luoda")
        return redirect("/project/" + str(project_id) + "/new-item")
    return redirect("/project/" + str(project_id) + "/item/" + str(item_id))

@app.route("/find-item")
def find_items():
    require_login()
    query = request.args.get("query")
    results = []
    if query:
        results = items.find_items(query)
    else:
        query = ""
    return render_template("find_item.html", query=query, results=results)

@app.route("/project/<int:project_id>/item/<int:item_id>")
def show_item(item_id, project_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("show_item.html", item=item, project_id = project_id)

@app.route("/edit-item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    return render_template("edit_item.html", item=item)

@app.route("/update-item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(400)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(400)
    items.update_item(item_id, title, description)
    return redirect("/project/" + str(item["project_id"]) + "/item/" + str(item_id))

@app.route("/remove-item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        return redirect("/project/" + str(item["project_id"]) + "/item/" + str(item_id))
    return render_template("remove_item.html", item=item)
