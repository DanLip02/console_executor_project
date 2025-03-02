from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os
from connection import connect_to_db

load_dotenv()

user = os.getenv("USER")
host = os.getenv("HOST")
port = int(os.getenv("PORT", "5433"))
password = os.getenv("PASSWORD")
db = os.getenv("DB")

def test_query(engine):
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()  
            if rows:
                for row in rows:
                    print(row)
            else:
                print("Таблица существует, но данных в ней нет.")
    except SQLAlchemyError as e:
        print(f"❌ Ошибка выполнения запроса: {e}")

schema = 'public'
table = 'employees'

query = f"SELECT * FROM {schema}.{table}"
engine = connect_to_db(user, host, port, password, db)

if engine:
    test_query(engine)