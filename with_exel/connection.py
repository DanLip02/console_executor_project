import os
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" \
               f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

engine = create_engine(DATABASE_URL)


def get_table_structure(table_name):
    try:
        inspector = inspect(engine)
        columns = inspector.get_columns(table_name)
        return {col["name"]: col["type"] for col in columns}
    except Exception as e:
        print(f"Ошибка при получении структуры таблицы: {e}")
        return None