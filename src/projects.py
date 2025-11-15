import db

def add_project(title, description):
    sql = """INSERT INTO Projects (title, description)
             VALUES (?, ?)"""
    db.execute(sql, [title, description])

def get_project(project_id):
    sql = """SELECT id,
                    title,
                    type,
                    description,
                    owner
             FROM Projects
             WHERE id = ?"""
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
    sql = """SELECT id, title, description
             FROM Projects
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    like = "%" + query + "%"
    return db.query(sql, [like, like])