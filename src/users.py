from werkzeug.security import generate_password_hash, check_password_hash

import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO Users (username, password_hash, created) VALUES (?, ?, datetime('now'))"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_all_users():
    sql = """SELECT id, username, created 
            FROM Users
            ORDER BY id DESC"""
    return db.query(sql)

def find_users(query):
    sql = """SELECT id, username, created 
            FROM Users
            WHERE username LIKE ?
            ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like])

def get_all_users():
    sql = "SELECT username FROM users"
    result = db.query(sql)
    return result[0] if result else None