from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from connection import *

def test_query():
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
test_query()