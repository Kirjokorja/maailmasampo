import db
import classes
import users

def add_item(title, description, user_id, class_id, project_id):
    action_id = classes.get_class('Tietokohdetoiminto','tietokohteen luominen')
    sql_items = """INSERT INTO Items (title, type, description, project)
                    VALUES (?, ?, ?, ?)"""
    sql_log = "INSERT INTO Log_items (actor, action, item_id, comment) VALUES (?, ?, ?, ?)"
    user = users.get_user(user_id)
    con = db.get_connection()
    con.execute("BEGIN")
    result = con.execute(sql_items, [title, class_id, description, project_id])
    new_item_id = result.lastrowid
    comment = f"Kohteen tunnus tietokannassa: {new_item_id}\n\
                Kohteen nimi: {title}\n\
                Luotu hankkeeseen: {project_id}\nLuonut: {user["username"]}"
    con.execute(sql_log, [user_id, action_id, new_item_id, comment])
    con.execute("COMMIT")
    con.close()
    return new_item_id

def get_item(item_id):
    sql = """SELECT Items.id,
                    Items.title,
                    Items.type,
                    Items.description,
                    Items.project project_id,
                    Projects.title project_name
             FROM Items, Projects
             WHERE Items.id = ? AND Items.project = Projects.id"""
    result = db.query(sql, [item_id])
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
    sql = """
             SELECT id, title, description
             FROM Items
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])
