CREATE TABLE urls (
    url_id SERIAL PRIMARY KEY, 
    http_path TEXT, 
    active TEXT,
    frequency 
)

CREATE TABLE paths (
    path_id SERIAL PRIMARY KEY,
    FOREIGN KEY (url_id) REFERENCES urls(url_id),
    json_path TEXT,


)


CREATE TABLE records (

)