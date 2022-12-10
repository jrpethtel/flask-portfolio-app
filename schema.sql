DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	title TEXT NOT NULL,
	summary TEXT NOT NULL,
	sourceLink TEXT,
	appLink TEXT
);