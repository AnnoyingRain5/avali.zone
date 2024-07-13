PRAGMA user_version = 3;

CREATE TABLE users
(
    id                   TEXT PRIMARY KEY,
    admin                BOOLEAN DEFAULT FALSE,
    golink_approved      BOOLEAN DEFAULT FALSE,
    manage_own_infoboxes BOOLEAN DEFAULT FALSE
);

CREATE TABLE categories
(
    id           INTEGER PRIMARY KEY,
    name         TEXT   NOT NULL,
    type         TEXT   NOT NULL,
    displayorder NUMBER NOT NULL
);

CREATE TABLE announcements
(
    id      INTEGER PRIMARY KEY,
    text    TEXT,
    enabled BOOLEAN DEFAULT TRUE
);

CREATE TABLE infoboxes
(
    id           INTEGER PRIMARY KEY,
    type         TEXT   NOT NULL,
    name         TEXT   NOT NULL,
    description  TEXT   NOT NULL,
    displayorder NUMBER NOT NULL,
    categoryid   NUMBER NOT NULL,
    owner        TEXT   NOT NULL,
    FOREIGN KEY (categoryid) REFERENCES categories (id),
    FOREIGN KEY (owner) REFERENCES users (id)
);

CREATE TABLE links
(
    id          INTEGER PRIMARY KEY,
    name        TEXT   NOT NULL,
    destination TEXT   NOT NULL,
    infoboxid   NUMBER NOT NULL
);

CREATE TABLE golinks
(
    name        TEXT PRIMARY KEY,
    destination TEXT NOT NULL,
    owner       TEXT NOT NULL,
    FOREIGN KEY (owner) REFERENCES users (id)
);

