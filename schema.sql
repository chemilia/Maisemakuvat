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
    scenery BLOB,
    user_id INTEGER REFERENCE users(id),
    mime_type TEXT,
    landscape_type_id INTEGER REFENCES landscape_types(id)
);

CREATE TABLE landscape_types (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    photo_id INTEGER REFERENCES photos(id),
    user_id INTEGER REFERENCES users(id)
);