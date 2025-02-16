CREATE TABLE boo(
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    author VARCHAR(30),
    price DECIMAL(8,2),
    amount INT
);
INSERT INTO boo (title, author, price, amount)
VALUES 
    ('Мастер и Маргарита', 'Булгаков М.А.', 670.99, 3),
    ('Белая гвардия', 'Булгаков М.А.', 540.50, 5),
    ('Идиот', 'Достоевский Ф.М.', 460.00, 10),
    ('Братья Карамазовы', 'Достоевский Ф.М.', 799.01, 2);

SELECT author, title, price, amount
FROM boo
WHERE amount BETWEEN 2 AND 14
ORDER BY author DESC, title;