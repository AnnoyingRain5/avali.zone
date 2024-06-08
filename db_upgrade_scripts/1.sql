ALTER TABLE categories ADD type TEXT NOT NULL DEFAULT 'group';

ALTER TABLE infobox RENAME TO infoboxes;


PRAGMA user_version = 2;