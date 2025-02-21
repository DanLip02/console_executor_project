CREATE TABLE bookrf(
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(50),
    author VARCHAR(30),
    price DECIMAL(8,2),
    amount INT
);
INSERT INTO bookrf (title, author, price, amount)
VALUES 
    ('Мастер и Маргарита', 'Булгаков М.А.', 670.99, 3),
    ('Белая гвардия', 'Булгаков М.А.', 540.50, 5),
    ('Идиот', 'Достоевский Ф.М.', 460.00, 10),
    ('Братья Карамазовы', 'Достоевский Ф.М.', 799.01, 2),
	('Стихотворения и поэмы', 'Есенин С.А.', 650.00, 15),
	('Лирика', 'Гумилев Н.С.', 460.00, 10),
	('Поэмы', 'Бехтерев С.С.', 460.00, 10),
	('Капитанская дочка', 'Пушкин А.С.', 520.50, 7),
	('Дети полуночи', 'Рушди Салман', 950.00, 5);

SELECT author, title, price, amount 
FROM boo
WHERE 
    title LIKE '% %'
    AND (
		amount BETWEEN 2 AND 14 
    	AND author LIKE '% С.%'
        OR author LIKE '%С.%'
    )
ORDER BY author DESC, title;