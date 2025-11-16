from werkzeug.security import generate_password_hash, check_password_hash

import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql_classes = "SELECT id FROM Classes WHERE title = ? AND value = ?"
    action = db.query(sql_classes, ["Käyttäjätoiminto", "käyttäjän luominen"])
    action_id = action[0]["id"]
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
                    datetime(Log_users.time, 'localtime') created
            FROM Users, Log_users
            WHERE Users.id = Log_users.actor
            AND Log_users.action = (SELECT id FROM Classes WHERE title = ? AND value = ?)
            AND Users.id = ?"""
    result = db.query(sql, ["Käyttäjätoiminto", "käyttäjän luominen", user_id])
    return result[0] if result else None

def find_users(query):
    sql = """SELECT Users.id,
                    Users.username, 
                    datetime(Log_users.time, 'localtime') created 
            FROM Users, Log_users
            WHERE Users.id = Log_users.actor 
            AND Log_users.action = (SELECT id FROM Classes WHERE title = ? AND value = ?) 
            AND Users.username LIKE ?
            ORDER BY Users.username DESC"""
    like = "%" + query + "%"
    return db.query(sql, ["Käyttäjätoiminto", "käyttäjän luominen", like])
