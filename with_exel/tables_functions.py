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

def create_table_from_file(table_name, file_path):
    try:
        # Определяем тип файла и загружаем данные
        if file_path.endswith(".csv"):
            df = engine.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = engine.read_excel(file_path)
        else:
            print("❌ Ошибка: Поддерживаются только файлы CSV и Excel.")
            return
        
        # Проверяем, что в файле есть данные
        if df.empty:
            print("❌ Ошибка: Файл пуст.")
            return
        
        with engine.connect() as conn:
            # Формируем SQL-запрос для создания таблицы
            columns_sql = ", ".join([f"{col} TEXT" for col in df.columns])
            query = text(f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY, {columns_sql})")
            conn.execute(query)
            
            # Загружаем данные в таблицу
            df.to_sql(table_name, con=engine, if_exists='append', index=False)
            print(f"✅ Таблица '{table_name}' создана и заполнена данными из файла '{file_path}'.")
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")

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