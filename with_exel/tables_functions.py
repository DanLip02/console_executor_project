from sqlalchemy import text
from connection import engine, DB_PARAMS
from with_excel import sys
import psycopg2


def create_table(table_name):
    column_defs = input("Введите названия колонок через запятую (например, name, age, email): ").strip()
    columns = [col.strip() for col in column_defs.split(",")]

    if not columns:
        print("❌ Ошибка: Нужно указать хотя бы одну колонку.")
        return

    with engine.connect() as conn:
        columns_sql = ", ".join([f"{col} TEXT" for col in columns])
        query = text(f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY, {columns_sql})")
        conn.execute(query)
        conn.commit()
        print(f"✅ Таблица '{table_name}' создана с колонками: {', '.join(columns)}")

def delete_table(table_name):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")

        conn.commit()
        print(f"Таблица '{table_name}' успешно удалена.")
    except psycopg2.Error as e:
        print(f"❌ Ошибка при удалении таблицы: {e}")
    finally:
        if conn:
            conn.close()