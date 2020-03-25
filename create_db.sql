CREATE TABLE urls (
  id serial,
  http varchar(100) NOT NULL UNIQUE,
  status varchar(100) NOT NULL,
  PRIMARY KEY (id)
);

/*
 one to many: Book has many reviews
*/

CREATE TABLE records (
  id serial,
  url_id integer NOT NULL,
  path text, 
  metric real,
  published_date timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  FOREIGN KEY (url_id) REFERENCES urls(id) ON DELETE CASCADE
);

