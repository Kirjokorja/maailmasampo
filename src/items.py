import db
import classes
import users
import projects

def add_item(title, description, user_id, class_id, project_id):
    action_id = classes.get_class_id('Tietokohdetoiminto','tietokohteen luominen')
    sql_items = """INSERT INTO Items (title, type, description, project)
                    VALUES (?, ?, ?, ?)"""
    sql_log = "INSERT INTO Log_items (actor, action, item_id, comment) VALUES (?, ?, ?, ?)"
    user = users.get_user(user_id)
    project = projects.get_project(project_id)
    con = db.get_connection()
    result = con.execute(sql_items, [title, class_id, description, project])
    new_item_id = result.lastrowid
    comment = create_item_log_comment(new_item_id, title, project, user)
    con.execute(sql_log, [user_id, action_id, new_item_id, comment])
    con.commit()
    con.close()
    return new_item_id

def create_item_log_comment(item_id, title, project, user):
    comment = f"Kohteen tunnus tietokannassa: {item_id}\n\
                Kohteen nimi: {title}\n\
                Luotu hankkeeseen: {project["title"]}\n\
                Hankkeen tunnus: {project["id"]}\n\
                Luonut: {user["username"]}\n\
                Luojan tunnus tietokannassa: {user["id"]}"
    return comment

def get_item(item_id):
    sql = """SELECT Items.id,
                    Items.title,
                    Classes.value type_value,
                    Items.project project_id,
                    Items.description,   
                    Projects.title project_name,
                    Users.id creator_id,
                    Users.username creator,
                    datetime(Log_items.time, 'localtime') created
             FROM Items, Projects, Log_items, Classes, Users
             WHERE Items.id = ? 
             AND Items.project = Projects.id
             AND Items.type = Classes.id
             AND Items.id = Log_items.item_id
             AND Log_items.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
             AND Log_items.actor = Users.id"""
    result = db.query(sql, [item_id, 'Tietokohdetoiminto', 'tietokohteen luominen'])
    return result[0] if result else None

def update_item(item_id, title, description):
    sql = """UPDATE Items SET title = ?,
                            description = ?
                            WHERE id = ?"""
    db.execute(sql, [title, description, item_id])

def remove_item(item_id):
    sql = "DELETE FROM Items WHERE id = ?"
    db.execute(sql, [item_id])

def find_items(query):
    sql = """SELECT id, title, description
             FROM Items
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
