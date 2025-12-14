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
    result = con.execute(sql_projects, [title, class_id, description, user_id])
    new_project_id = result.lastrowid
    comment = create_project_log_comment(new_project_id, title, user)
    con.execute(sql_log, [user_id, action_id, new_project_id, comment])
    con.commit()
    con.close()
    return new_project_id

def create_project_log_comment(project_id, title, user):
    comment = f"Hankkeen tunnus tietokannassa: {project_id}\n\
                Hankkeen nimi: {title}\n\
                Luonut: {user["username"]}\n\
                Luojan tunnus tietokannassa: {user["id"]}"
    return comment

def get_project(project_id):
    sql = """SELECT Projects.id,
                    Projects.title,
                    Classes.value type_value,
                    Projects.description,
                    Users.id owner_id,
                    Users.username owner_name,
                    datetime(Log_projects.time, 'localtime') created
             FROM Projects, Users, Log_projects, Classes
             WHERE Users.id = Projects.owner 
             AND Projects.id = ?
             AND Projects.id = Log_projects.project_id
             AND Classes.id = Projects.type
             AND Log_projects.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)"""
    result = db.query(sql, [project_id, 'Hanketoiminto', 'hankkeen luominen'])
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
             ORDER BY id"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, 'Hanketoiminto', 'hankkeen luominen'])

def get_project_log(project_id):
    sql = "SELECT * FROM Log_projects WHERE project_id = ?"
    return db.query(sql, [project_id])

def count_projects_items(query):
    sql = """SELECT
                (SELECT COUNT(*) FROM Projects 
                                WHERE (Projects.title LIKE ? OR Projects.description LIKE ?))
                +
                (SELECT COUNT(*) FROM Items 
                                WHERE (Items.title LIKE ? OR Items.description LIKE ?))"""
    like = "%" + query + "%"
    return db.query(sql, [like, like, like, like])[0][0]

def find_projects_items(query, page, page_size):
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
             ORDER BY title ASC
             LIMIT ? OFFSET ?"""
    like = "%" + query + "%"
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [like, like, 'Hanketoiminto', 'hankkeen luominen',
                          like, like, 'Tietokohdetoiminto', 'tietokohteen luominen', limit, offset])
