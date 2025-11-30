from werkzeug.security import generate_password_hash, check_password_hash

import db
import classes
import exceptions

def log_user(user_id, action_id):
    sql_log = "INSERT INTO Log_users (actor, action) VALUES (?, ?)"
    db.execute(sql_log, [user_id, action_id])

def create_user(username, password):
    user_check_query = "SELECT username FROM Users WHERE username = ?"
    user_check = db.query(user_check_query, [username])
    print(user_check)
    if user_check:
        raise exceptions.UserAlreadyExists(f"Database found user {user_check[0]}.")
    password_hash = generate_password_hash(password)
    action_id = classes.get_class_id('Käyttäjätoiminto', 'käyttäjän luominen')
    sql_users = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
    sql_log = "INSERT INTO Log_users (actor, action) VALUES (?, ?)"
    con = db.get_connection()
    con.execute("BEGIN")
    result = con.execute(sql_users, [username, password_hash])
    new_user_id = result.lastrowid
    con.execute(sql_log, [new_user_id, action_id])
    con.execute("COMMIT")
    con.close()

def check_login(username, password):
    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    if result:
        user_id = result[0]["id"]
        password_hash = result[0]["password_hash"]
        if check_password_hash(password_hash, password):
            return user_id
    return None

def get_user(user_id):
    sql = """SELECT Users.id,
                    Users.username,
                    datetime(Log_users.time, 'localtime') created,
                    count(Projects.id) projects_owned,
                    count(Log_items.id) number_of_items
            FROM Users, Log_users, Projects, Log_items
            WHERE Users.id = Log_users.actor
            AND Log_users.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
            AND Projects.owner = ?
            AND Log_items.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
            AND Users.id = ?"""
    result = db.query(sql, ["Käyttäjätoiminto", "käyttäjän luominen", user_id,
                            'Tietokohdetoiminto', 'tietokohteen luominen', user_id])
    return result[0] if result else None

def find_users(query):
    sql = """SELECT Users.id,
                    Users.username,
                    datetime(Log_users.time, 'localtime') created,
                    count(Projects.id) projects_owned,
                    count(Log_items.id) number_of_items
            FROM Users, Log_users, Projects, Log_items
            WHERE Users.id = Log_users.actor 
            AND Log_users.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
            AND Projects.owner = Users.id
            AND Log_items.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
            AND Users.username LIKE ?
            ORDER BY Users.username DESC"""
    like = "%" + query + "%"
    return db.query(sql, ["Käyttäjätoiminto", "käyttäjän luominen",
                          'Tietokohdetoiminto', 'tietokohteen luominen', like])

def get_user_items(user_id):
    sql = """SELECT Items.id,
                    Items.title,
                    Classes.value type_value,
                    Items.description,
                    Items.project project_id,
                    Projects.title project_name,
                    datetime(Log_items.time, 'localtime') created
             FROM Items, Projects, Log_items, Classes
             WHERE Log_items.actor = ?
             AND Items.project = Projects.id
             AND Items.type = Classes.id
             AND Items.id = Log_items.item_id
             AND Log_items.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
             ORDER BY created DESC"""
    return db.query(sql, [user_id, 'Tietokohdetoiminto', 'tietokohteen luominen'])
