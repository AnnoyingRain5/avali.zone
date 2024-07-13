CREATE TABLE categories
(
    id           INTEGER PRIMARY KEY,
    name         TEXT   NOT NULL,
    displayorder NUMBER NOT NULL
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


PRAGMA user_version = 1;