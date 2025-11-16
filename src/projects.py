import db

def get_all_classes():
    sql = """SELECT id, value FROM Classes
            WHERE title = ?
            ORDER BY id"""
    result = db.query(sql, ['Hanke'])
    classes = {}
    for class_id, class_value in result:
        classes[class_id] = [class_value]
    return classes

def get_class_value(class_id):
    sql = """SELECT id, value FROM Classes
            WHERE id = ?"""
    result = db.query(sql, [class_id])
    return result

def add_project(title, description, user_id, class_id):
    sql_classes = "SELECT id FROM Classes WHERE title = ? AND value = ?"
    action = db.query(sql_classes, ["Hanketoiminto", "hankkeen luominen"])
    action_id = action[0]["id"]
    sql_projects = """INSERT INTO Projects (title, type, description, owner)
                    VALUES (?, ?, ?, ?)"""
    sql_log = "INSERT INTO Log_projects (actor, action, project_id) VALUES (?, ?, ?)"
    con = db.get_connection()
    con.execute("BEGIN")
    result = con.execute(sql_projects, [title, class_id, description, user_id])
    new_project_id = result.lastrowid
    con.execute(sql_log, [user_id, action_id, new_project_id])
    con.execute("COMMIT")
    con.close()
    return new_project_id

def get_project(project_id):
    sql = """SELECT Projects.id,
                    Projects.title,
                    Projects.type,
                    Projects.description,
                    Users.id owner_id,
                    Users.username owner_name
             FROM Projects, Users
             WHERE Users.id = Projects.owner AND Projects.id = ?"""
    result = db.query(sql, [project_id])
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
    sql = """SELECT id, title
             FROM Projects
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
