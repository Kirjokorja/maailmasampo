CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    created DATETIME
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
    project INTEGER REFERENCES Projects
);

CREATE TABLE Subitems (
    id INTEGER PRIMARY KEY,
    title TEXT,
    type INTEGER REFERENCES Classes,
    description TEXT,
    item INTEGER REFERENCES Items
);

CREATE TABLE Members (
    project INTEGER REFERENCES Projects,
    member INTEGER REFERENCES Users
);

CREATE TABLE Log (
    time DATETIME,
    actor INTEGER REFERENCES Users,
    action INTEGER REFERENCES Classes,
    data_type TEXT,
    data_id INTEGER
);

CREATE TABLE Classes (
    id INTEGER PRIMARY KEY,
    title TEXT, --'hanke', 'toiminto', 'luokka'
    value TEXT --'hanke'{'maailma'}, 'toiminto'{'sisäänkirjaus', 'uloskirjaus', 'käyttäjän luonti', 'käyttäjän hävitys', 
                -- 'hankkeen luonti', 'hankkeen haltijan muutos', 'hankkeen muokkaus', 'hankkeen hävittäminen', 'tietokohteen luominen', 
                -- 'tietokohteen hävittäminen', 'tietokohteen muokkaus', 'käyttäjän lisäys hankkeeseen', 'käyttäjän poisto hankkeeesta', '},
                -- 'luokka' {'alue', 'ympäristö', 'luonnonlaki', 'paikka', 'kulttuuri', 'yhteisö', 'laji', 'olento', 'henkilö', 'esine', 'menetelmä'}
);