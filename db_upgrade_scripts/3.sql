CREATE TABLE announcements
(
    id      INTEGER PRIMARY KEY,
    text    TEXT,
    enabled BOOLEAN DEFAULT TRUE
);

PRAGMA user_version = 4;