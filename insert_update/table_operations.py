import sys
import json
from connection import engine
from sqlalchemy import text


def get_columns(table): #список столбцов
    with engine.connect() as conn:
        query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table}'")
        result = conn.execute(query)
        return [row[0] for row in result]


def insert_data(table, data): #вставка данных
    columns = get_columns(table)

    # Проверка на соответствие переданных данных столбцам таблицы
    invalid_columns = [key for key in data.keys() if key not in columns]
    if invalid_columns:
        print(f"❌ Ошибка: Столбцы {', '.join(invalid_columns)} отсутствуют в таблице {table}.")
        return

    with engine.connect() as conn:
        column_names = ", ".join(data.keys())
        values = ", ".join([f":{key}" for key in data.keys()])
        query = text(f"INSERT INTO {table} ({column_names}) VALUES ({values})")
        conn.execute(query, data)
        conn.commit()
        print("✅ Данные успешно вставлены!")


def update_data(table, data, condition): 
    columns = get_columns(table)

    # Проверка на соответствие переданных данных столбцам таблицы
    invalid_columns = [key for key in data.keys() if key not in columns]
    if invalid_columns:
        print(f"❌ Ошибка: Столбцы {', '.join(invalid_columns)} отсутствуют в таблице {table}.")
        return

    set_values = ", ".join([f"{key} = :{key}" for key in data.keys()])
    where_condition = " AND ".join([f"{key} = :{key}" for key in condition.keys()])

    with engine.connect() as conn:
        query = text(f"UPDATE {table} SET {set_values} WHERE {where_condition}")
        conn.execute(query, {**data, **condition})
        conn.commit()
        print("✅ Данные успешно обновлены!")


def delete_data(table, condition): #удаление данных
    columns = get_columns(table)

    # Проверка на соответствие переданных данных столбцам таблицы
    invalid_columns = [key for key in condition.keys() if key not in columns]
    if invalid_columns:
        print(f"❌ Ошибка: Столбцы {', '.join(invalid_columns)} отсутствуют в таблице {table}.")
        return

    where_condition = " AND ".join([f"{key} = :{key}" for key in condition.keys()])

    with engine.connect() as conn:
        query = text(f"DELETE FROM {table} WHERE {where_condition}")
        conn.execute(query, condition)
        conn.commit()
        print("✅ Данные успешно удалены!")


def main():
    print("Выберите операцию: вставка, обновление, удаление")
    operation = input("Введите операцию: ").strip().lower()

    if operation not in ["вставка", "обновление", "удаление"]:
        print("❌ Ошибка: Неверная операция!")
        sys.exit(1)

    table = input("Введите название таблицы: ").strip()

    if operation == "вставка":
        data = input("Введите данные в JSON-формате: ").strip()
        insert_data(table, json.loads(data))

    elif operation == "обновление":
        data = input("Введите новые данные в JSON-формате: ").strip()
        condition = input("Введите условия обновления в JSON-формате: ").strip()
        update_data(table, json.loads(data), json.loads(condition))

    elif operation == "удаление":
        condition = input("Введите условия удаления в JSON-формате: ").strip()
        delete_data(table, json.loads(condition))


if __name__ == "__main__":
    main()