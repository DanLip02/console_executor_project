CREATE TABLE employees (
    id SERIAL PRIMARY KEY,   
    name VARCHAR(100),       
    manager_id INT NULL,     -- Manager ID (link to another employee’s ID)
    FOREIGN KEY (manager_id) REFERENCES employees(id)
);

INSERT INTO employees (id, name, manager_id) VALUES
(1, 'Директор', NULL),         -- The top level has no boss (NULL)
(2, 'Заместитель директора', 1),
(3, 'Главный инженер', 1),
(4, 'Начальник отдела IT', 2),
(5, 'Начальник отдела продаж', 2),
(6, 'Разработчик', 4),
(7, 'Системный администратор', 4),
(8, 'Менеджер по продажам', 5),
(9, 'Специалист по маркетингу', 5);

WITH RECURSIVE employee_hierarchy AS (
    SELECT id, name, manager_id, 1 AS level
    FROM employees
    WHERE manager_id IS NULL 

    UNION ALL

    SELECT e.id, e.name, e.manager_id, eh.level + 1
    FROM employees e
    JOIN employee_hierarchy eh ON e.manager_id = eh.id
)
SELECT * FROM employee_hierarchy
ORDER BY level, name;