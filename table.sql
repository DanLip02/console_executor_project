CREATE TABLE pep (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    age INT
);
INSERT INTO pep (name, age) VALUES ('Alice', 25), ('Bob', 30);
SELECT * FROM pep;