from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Подключение к БД
user = "postgres"
host = "localhost"
port = "5433"
password = ""
db = "ela"

engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

def test_query():
    try:
        with engine.connect() as connection:
            connection.execute(text("SET search_path TO public;"))
            result = connection.execute(text("SELECT * FROM employees;"))
            rows = result.fetchall()  
            if rows:
                for row in rows:
                    print(row)
            else:
                print("Таблица существует, но данных в ней нет.")
    except SQLAlchemyError as e:
        print(f"❌ Ошибка выполнения запроса: {e}")

test_query()