from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def connect_to_db(user, host, port, password, db):
    try:
        engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
        with engine.connect() as connection:
            connection.execute(text("SELECT 1")) 
        print("✅ Подключение успешно!")
        return engine
    except SQLAlchemyError as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return None
