CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE photos (
    id INTEGER PRIMARY KEY, 
    seasons TEXT, 
    era INTEGER,
    description TEXT, 
    user_id INTEGER REFERENCE users, 
);