DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS scene;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE scene (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  participants TEXT NOT NULL,
  location TEXT NOT NULL,
  music TEXT,
  dramatic_poles TEXT,
  emotional_requests TEXT,

  FOREIGN KEY (user_id) REFERENCES user (id)
);