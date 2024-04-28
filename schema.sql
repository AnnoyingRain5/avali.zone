CREATE TABLE users (
  id              TEXT PRIMARY KEY,
  admin           BOOLEAN DEFAULT FALSE,
  golink_approved BOOLEAN DEFAULT FALSE
);

CREATE TABLE golinks (
  name TEXT   PRIMARY KEY,
  destination TEXT NOT NULL,
  owner       TEXT NOT NULL,
  FOREIGN KEY(owner) REFERENCES user(id)
);

