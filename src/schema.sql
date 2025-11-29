CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE Projects (
    id INTEGER PRIMARY KEY,
    title TEXT, 
    type INTEGER REFERENCES Classes,
    description TEXT,
    owner INTEGER REFERENCES Users
);

CREATE TABLE Items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    type INTEGER REFERENCES Classes,
    description TEXT,
    project INTEGER REFERENCES Projects ON DELETE CASCADE
);

CREATE TABLE Subitems (
    id INTEGER PRIMARY KEY,
    title TEXT,
    type INTEGER REFERENCES Classes,
    description TEXT,
    item INTEGER REFERENCES Items
);

CREATE TABLE Members (
    id INTEGER PRIMARY KEY,
    project INTEGER REFERENCES Projects ON DELETE CASCADE,
    member INTEGER REFERENCES Users
);

CREATE TABLE Log_users (
    id INTEGER PRIMARY KEY,
    time TEXT DEFAULT CURRENT_TIMESTAMP,
    actor INTEGER REFERENCES Users,
    action INTEGER REFERENCES Classes,
    comment TEXT
);

CREATE TABLE Log_projects (
    id INTEGER PRIMARY KEY,
    time TEXT DEFAULT CURRENT_TIMESTAMP,
    actor INTEGER REFERENCES Users,
    action INTEGER REFERENCES Classes,
    project_id INTEGER REFERENCES Projects ON DELETE SET NULL,
    comment TEXT
);

CREATE TABLE Log_items (
    id INTEGER PRIMARY KEY,
    time TEXT DEFAULT CURRENT_TIMESTAMP,
    actor INTEGER REFERENCES Users,
    action INTEGER REFERENCES Classes,
    item_id INTEGER REFERENCES Items ON DELETE SET NULL,
    comment TEXT
);

CREATE TABLE Classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);