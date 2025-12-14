import random
import string

from werkzeug.security import generate_password_hash

import classes
import db
import projects
import items

project_class_id = classes.get_class_id('Hanke','maailma')
user_action_id = classes.get_class_id('Käyttäjätoiminto', 'käyttäjän luominen')
project_action_id = classes.get_class_id('Hanketoiminto','hankkeen luominen')
item_action_id = classes.get_class_id('Tietokohdetoiminto','tietokohteen luominen')
all_classes = classes.get_all_classes('Luokka')
class_list = list(all_classes)
con = db.get_connection()

con.execute("DELETE FROM Projects")
con.execute("DELETE FROM Users")
con.execute("DELETE FROM Items")
con.execute("DELETE FROM Log_users")
con.execute("DELETE FROM Log_projects")
con.execute("DELETE FROM Log_items")


USER_COUNT = 10**3
PROJECTS_COUNT = 10**4
ITEMS_COUNT = 10**5

def randomtext(length):
    chars = string.printable
    return ''.join(random.choice(chars) for i in range(length))

for i in range(1, USER_COUNT + 1):
    sql_user = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
    sql_log = "INSERT INTO Log_users (actor, action) VALUES (?, ?)"
    password_hash = generate_password_hash("moikka")
    username = "Käyttäjä" + str(i)
    result = con.execute(sql_user, [username, password_hash])
    new_user_id = result.lastrowid
    con.execute(sql_log, [new_user_id, user_action_id])

for i in range(1, PROJECTS_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    username = "Käyttäjä" + str(user_id)
    user = {"id": user_id, "username": username}
    text_lenght = random.randint(0, 80)
    title = "Maailma" + str(i)
    sql_projects = "INSERT INTO Projects (title, type, description, owner) VALUES (?, ?, ?, ?)"
    sql_log = "INSERT INTO Log_projects (actor, action, project_id, comment) VALUES (?, ?, ?, ?)"
    result = con.execute(sql_projects, [title, project_class_id, randomtext(text_lenght),user_id])
    new_project_id = result.lastrowid
    comment = projects.create_project_log_comment(new_project_id, title, user)
    con.execute(sql_log, [user_id, project_action_id, new_project_id, comment])

for i in range(1, ITEMS_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    username = "Käyttäjä" + str(user_id)
    user = {"id": user_id, "username": username}
    text_lenght = random.randint(0, 80)
    random_class = random.randint(0, len(class_list)-1)
    class_id = class_list[random_class]
    project_id = random.randint(1, PROJECTS_COUNT)
    project_name = "Maailma" + str(user_id)
    project = {"id": project_id, "title": project_name}
    title = "Kohde" + str(i)
    sql_items = "INSERT INTO Items (title, type, description, project) VALUES (?, ?, ?, ?)"
    sql_log = "INSERT INTO Log_items (actor, action, item_id, comment) VALUES (?, ?, ?, ?)"
    result = con.execute(sql_items, [title, class_id, randomtext(text_lenght), project_id])
    new_item_id = result.lastrowid
    comment = items.create_item_log_comment(new_item_id, title, project, user)
    con.execute(sql_log, [user_id, item_action_id, new_item_id, comment])

con.commit()
con.close()
