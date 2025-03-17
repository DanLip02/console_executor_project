import sys
import pandas as pd
from connection import engine
from sqlalchemy import text

def get_columns(table):
    with engine.connect() as conn:
        query = text("SELECT column_name FROM information_schema.columns WHERE table_name = :table")
        result = conn.execute(query, {"table": table})
        columns = [row[0] for row in result]
        return [col for col in columns if col.lower() != "id"]

def parse_input(input_str, columns):
    values = [item.strip() for item in input_str.split(',')]
    if len(values) != len(columns):
        print(f"❌ Ошибка: Ожидалось {len(columns)} значений, но получено {len(values)}.")
        return None
    return dict(zip(columns, values))

def insert_data_to_excel(file_path, data):
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        df = pd.DataFrame(columns=data.keys())

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_excel(file_path, index=False)
    print("✅ Данные успешно добавлены в Excel")

def delete_data_from_excel(file_path, condition):
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print("❌ Файл Excel не найден.")
        return
    for key, value in condition.items():
        df = df[df[key] != value]
    df.to_excel(file_path, index=False)
    print("✅ Данные успешно удалены из Excel")

def insert_data(table, data):  # Вставка данных
    with engine.connect() as conn:
        column_names = ", ".join(data.keys())
        values_placeholders = ", ".join([f":{key}" for key in data.keys()])
        query = text(f"INSERT INTO {table} ({column_names}) VALUES ({values_placeholders})")
        conn.execute(query, data)
        conn.commit()
        print("✅ Данные успешно вставлены")

def update_data(table, data, condition):  # Обновление данных
    set_values = ", ".join([f"{key} = :{key}" for key in data.keys()])
    where_condition = " AND ".join([f"{key} = :cond_{key}" for key in condition.keys()])
    with engine.connect() as conn:
        query = text(f"UPDATE {table} SET {set_values} WHERE {where_condition}")
        query_params = {**data, **{f"cond_{k}": v for k, v in condition.items()}}
        conn.execute(query, query_params)
        conn.commit()
        print("✅ Данные успешно обновлены")

def delete_data(table, condition):  # Удаление данных
    where_condition = " AND ".join([f"{key} = :{key}" for key in condition.keys()])
    with engine.connect() as conn:
        query = text(f"DELETE FROM {table} WHERE {where_condition}")
        conn.execute(query, condition)
        conn.commit()
        print("✅ Данные успешно удалены")

def main():
    print("Выберите операцию: вставка sql, удаление sql, обновление sql, вставка в Excel, удаление из Excel")
    operation = input("Введите операцию: ").strip().lower()
    
    if operation in ["вставка в excel", "удаление из excel"]:
        file_path = input("Введите путь к файлу Excel: ").strip()
        columns = ["name", "age"]  
        if operation == "вставка в excel":
            data_input = input(f"Введите данные ({', '.join(columns)}): ").strip()
            data = parse_input(data_input, columns)
            if data:
                insert_data_to_excel(file_path, data)
        else:
            condition = parse_input(condition_input, columns)
            if condition:
                delete_data_from_excel(file_path, condition)
    
    elif operation in ["вставка sql", "обновление sql", "удаление sql"]:
        table = "users"
        columns = get_columns(table)
        if not columns:
            print(f"❌ Ошибка: Таблица {table} не найдена.")
            sys.exit(1)

        if operation == "вставка sql":
            data_input = input(f"Введите данные ({', '.join(columns)}): ").strip()
            data = parse_input(data_input, columns)
            if data:
                insert_data(table, data)

        elif operation == "обновление sql":
            data_input = input(f"Введите новые данные ({', '.join(columns)}): ").strip()
            condition_input = input(f"Введите условия обновления (например, name: Алиса): ").strip()
            data = parse_input(data_input, columns)
            condition = parse_input(condition_input, columns)
            if data and condition:
                update_data(table, data, condition)

        elif operation == "удаление sql":
            condition_input = input(f"Введите условия удаления (например, name: Алиса): ").strip()
            condition = parse_input(condition_input, columns)
            if condition:
                delete_data(table, condition)
    else:
        print("❌ Ошибка: Неверная операция")
        sys.exit(1)

if __name__ == "__main__":
    main()
