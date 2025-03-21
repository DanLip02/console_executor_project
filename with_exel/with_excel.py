import sys
from connection import engine
from sqlalchemy import text
from conn_files import *


def get_columns(table):  # Получаем список столбцов, исключая id
    with engine.connect() as conn:
        query = text("SELECT column_name FROM information_schema.columns WHERE table_name = :table")
        result = conn.execute(query, {"table": table})
        columns = [row[0] for row in result]
        return [col for col in columns if col.lower() != "id"]  # Исключаем id


def parse_input(input_str, columns):  # ввод пользователя в словарь
    values = [item.strip() for item in input_str.split(',')]
    if len(values) != len(columns):
        print(f"❌ Ошибка: Ожидалось {len(columns)} значений, но получено {len(values)}.")
        return None
    return dict(zip(columns, values))


def insert_data(table, data):  # Вставка данных
    columns = get_columns(table)

    if not columns:
        print(f"❌ Ошибка: Таблица {table} не найдена.")
        return

    with engine.connect() as conn:
        column_names = ", ".join(data.keys())
        values_placeholders = ", ".join([f":{key}" for key in data.keys()])
        query = text(f"INSERT INTO {table} ({column_names}) VALUES ({values_placeholders})")
        conn.execute(query, data)
        conn.commit()
        print("✅ Данные успешно вставлены")


def update_data(table, data, condition):  # Обновление данных
    columns = get_columns(table)

    if not columns:
        print(f"❌ Ошибка: Таблица {table} не найдена.")
        return

    set_values = ", ".join([f"{key} = :{key}" for key in data.keys()])
    where_condition = " AND ".join([f"{key} = :cond_{key}" for key in condition.keys()])

    with engine.connect() as conn:
        query = text(f"UPDATE {table} SET {set_values} WHERE {where_condition}")
        query_params = {**data, **{f"cond_{k}": v for k, v in condition.items()}}
        conn.execute(query, query_params)
        conn.commit()
        print("✅ Данные успешно обновлены")


def delete_data(table, condition):  # Удаление данных
    columns = get_columns(table)

    if not columns:
        print(f"❌ Ошибка: Таблица {table} не найдена.")
        return

    where_condition = " AND ".join([f"{key} = :{key}" for key in condition.keys()])

    with engine.connect() as conn:
        query = text(f"DELETE FROM {table} WHERE {where_condition}")
        conn.execute(query, condition)
        conn.commit()
        print("✅ Данные успешно удалены")


def main():
    print("Выберите операцию: вставка, обновление, удаление, вставка myfile, удаление myfile")
    operation = input("Введите операцию: ").strip().lower()

    if operation not in ["вставка", "обновление", "удаление", "вставка myfile", "удаление myfile"]:
        print("❌ Ошибка: Неверная операция")
        sys.exit(1)

    table = "users"
    columns = get_columns(table)
    create_table()

    if not columns:
        print(f"❌ Ошибка: Таблица {table} не найдена.")
        sys.exit(1)

    if operation == "вставка":
        data_input = input(f"Введите данные ({', '.join(columns)}): ").strip()
        data = parse_input(data_input, columns)
        if data:
            insert_data(table, data)

    elif operation == "обновление":
        data_input = input(f"Введите новые данные ({', '.join(columns)}): ").strip()
        condition_input = input(f"Введите условия обновления (например, name: Алиса): ").strip()
        data = parse_input(data_input, columns)
        condition = parse_input(condition_input, columns)
        if data and condition:
            update_data(table, data, condition)

    elif operation == "удаление":
        condition_input = input(f"Введите условия удаления (например, name: Алиса): ").strip()
        condition = parse_input(condition_input, columns)
        if condition:
            delete_data(table, condition)

    elif operation == "вставка myfile":
        file_path = input("Введите путь к файлу для загрузки: ").strip()
        excel_pull(file_path)
    elif operation == "удаление myfile":
        file_id = input("Введите ID файла для извлечения: ").strip()
        if file_id.isdigit():
            download_file(int(file_id))

if __name__ == "__main__":
    main()