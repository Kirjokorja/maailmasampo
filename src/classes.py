import db

def get_all_classes(class_title):
    sql = """SELECT id, value FROM Classes
            WHERE title = ?
            ORDER BY id"""
    result = db.query(sql, [class_title])
    classes = {}
    for class_id, class_value in result:
        classes[class_id] = class_value
    return classes

def get_class_value(class_id):
    sql = """SELECT id, value FROM Classes
            WHERE id = ?"""
    result = db.query(sql, [class_id])
    return result

def get_class_id(class_title, class_value):
    sql_classes = "SELECT id FROM Classes WHERE title = ? AND value = ?"
    action = db.query(sql_classes, [class_title, class_value])
    return action[0]["id"]
