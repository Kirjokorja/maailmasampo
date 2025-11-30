import db
import classes
import users

def add_project(title, description, user_id, class_id):
    action_id = classes.get_class_id('Hanketoiminto','hankkeen luominen')
    sql_projects = """INSERT INTO Projects (title, type, description, owner)
                    VALUES (?, ?, ?, ?)"""
    sql_log = "INSERT INTO Log_projects (actor, action, project_id, comment) VALUES (?, ?, ?, ?)"
    user = users.get_user(user_id)
    con = db.get_connection()
    con.execute("BEGIN")
    result = con.execute(sql_projects, [title, class_id, description, user_id])
    new_project_id = result.lastrowid
    comment = f"Hankkeen tunnus tietokannassa: {new_project_id}\n\
                Hankkeen nimi: {title}\n\
                Luonut: {user["username"]}"
    con.execute(sql_log, [user_id, action_id, new_project_id, comment])
    con.execute("COMMIT")
    con.close()
    return new_project_id

def get_project(project_id):
    sql = """SELECT Projects.id,
                    Projects.title,
                    Classes.value type_value,
                    Projects.description,
                    Users.id owner_id,
                    Users.username owner_name,
                    datetime(Log_projects.time, 'localtime') created,
                    count(Items.id) number_of_items
             FROM Projects, Users, Log_projects, Classes, Items
             WHERE Users.id = Projects.owner AND Projects.id = ?
             AND Projects.id = Log_projects.project_id
             AND Classes.id = Projects.type
             AND Log_projects.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
             AND Items.project = ?"""
    result = db.query(sql, [project_id, 'Hanketoiminto', 'hankkeen luominen', project_id])
    return result[0] if result else None

def update_project(project_id, title, description):
    sql = """UPDATE Projects SET title = ?,
                            description = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, project_id])

def remove_project(project_id):
    sql = "DELETE FROM Projects WHERE id = ?"
    db.execute(sql, [project_id])

def find_projects(query):
    sql = """SELECT id,
                    title, 
                    description, 
                    datetime(Log_projects.time, 'localtime') created
             FROM Projects, Log_projects
             WHERE (title LIKE ? OR description LIKE ?)
             AND Projects.id = Log_projects.project_id
             AND Log_projects.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, 'Hanketoiminto', 'hankkeen luominen'])

def get_project_log(project_id):
    sql = "SELECT * FROM Log_projects WHERE project_id = ?"
    return db.query(sql, [project_id])

def find_projects_items(query):
    sql = """SELECT Projects.id id,
                    Projects.title title,
                    Projects.description description,
                    Classes.title type,
                    Classes.value type_value,
                    Projects.id project_id,
                    Users.id owner_id,
                    Users.username owner_name,
                    datetime(Log_projects.time, 'localtime') created
             FROM Projects, Classes, Log_projects, Users
             WHERE (Projects.title LIKE ? OR Projects.description LIKE ?)
             AND Users.id = Projects.owner
             AND Projects.type = Classes.id
             AND Projects.id = Log_projects.project_id
             AND Log_projects.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
             UNION
             SELECT Items.id id,
                    Items.title title,
                    Items.description description,
                    Classes.title type,
                    Classes.value type_value,
                    Items.project project_id,
                    Users.id owner_id,
                    Users.username owner_name,
                    datetime(Log_items.time, 'localtime') created
             FROM Items, Classes, Log_items, Users
             WHERE (Items.title LIKE ? OR Items.description LIKE ?)
             AND Items.type = Classes.id
             AND Items.id = Log_items.item_id
             AND Log_items.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
             AND Log_items.actor = Users.id
             ORDER BY title DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, 'Hanketoiminto', 'hankkeen luominen',
                          like, like, 'Tietokohdetoiminto', 'tietokohteen luominen'])
