ALTER TABLE users
    ADD manage_own_infoboxes BOOLEAN DEFAULT FALSE;

PRAGMA user_version = 3;