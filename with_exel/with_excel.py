import sys
from connection import engine
from sqlalchemy import text
from conn_files import *
from tables_functions import *


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


def insert_data(table, data): 
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


def update_data(table, data, condition):
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


def delete_data(table, condition):
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
    print("Выберите операцию:\n Вставка\n Обновление\n Удаление\n Вставка myfile\n Удаление myfile\n Добавить элемент в файл\n Убрать элемент из файла\n")
    operation = input("Введите операцию: ").strip()

    allowed_operations = ["Вставка", "Обновление", "Удаление", "Вставка myfile", "Удаление myfile", "Добавить элемент в файл", "Убрать элемент из файла"]
    
    if operation not in allowed_operations:
        print("❌ Ошибка: Неверная операция")
        sys.exit(1)

    if operation == "Вставка":
        table = input("Введите название существующей таблицы (если хотите создать новую, нажмите Enter): ").strip()

        if not table:  
            table = input("Введите имя новой таблицы: ").strip()
            create_table(table)  

        columns = get_columns(table)  

        if not columns:
            print(f"❌ Ошибка: Не удалось получить колонки таблицы '{table}'. Возможно, она не была создана.")
            sys.exit(1)

        data_input = input(f"Введите данные ({', '.join(columns)}): ").strip()
        values = [item.strip() for item in data_input.split(",")]
        # data = parse_input(data_input, columns)
        # if data:
        #     insert_data(table, data)
        if len(values) != len(columns):
            print(f"❌ Ошибка: Ожидалось {len(columns)} значений, но получено {len(values)}.")
            sys.exit(1)

        data = dict(zip(columns, values))
        insert_data(table, data)

    elif operation == "обновление":
        data_input = input(f"Введите новые данные ({', '.join(columns)}): ").strip()
        condition_input = input(f"Введите условия обновления (например, name: Алиса): ").strip()
        data = parse_input(data_input, columns)
        condition = parse_input(condition_input, columns)
        if data and condition:
            update_data(table, data, condition)


    elif operation == "Удаление":
        table = input("Введите название таблицы: ").strip()

        if not table:
            print("❌ Ошибка: имя таблицы не может быть пустым.")
            sys.exit(1)

        delete_option = input(f"Удалить всю таблицу '{table}' или только данные? (введите 'таблица' или 'данные'): ").strip().lower()

        if delete_option == "таблица":
            confirm = input(f"Вы уверены, что хотите удалить таблицу '{table}'? (да/нет): ").strip().lower()
            if confirm == "да":
                delete_table(table)
                print(f"✅ Таблица '{table}' удалена.")
            else:
                print("❌ Операция отменена.")
        elif delete_option == "данные":
            condition_input = input("Введите условия удаления (например, id=5): ").strip()
            condition = parse_input(condition_input, get_columns(table))

            if condition:
                delete_data(table, condition)
                print(f"✅ Данные из таблицы '{table}' удалены по условию: {condition_input}")
            else:
                print("❌ Ошибка: условия удаления не заданы.")
        else:
            print("❌ Ошибка: неверный ввод. Введите 'таблица' или 'данные'.")

    elif operation == "вставка myfile":
        create_table()
        file_path = input("Введите путь к файлу для загрузки: ").strip()
        excel_pull(file_path)
    elif operation == "удаление myfile":
        file_id = input("Введите ID файла для извлечения: ").strip()
        if file_id.isdigit():
            download_file(int(file_id))
        else:
            print("ID должен быть числом. Ошибка")

    elif operation == "добавить элемент в файл":
        file_id = input("Введите ID файла: ").strip()
        new_data = input("Введите данные для добавления: ")
        if file_id.isdigit():
            update_file(int(file_id), new_data)
        else:
            print("Ошибка! Введите число!")

    elif operation == "убрать элемент из файла":
        file_id = input("Введите ID файла: ").strip()
        remove = input("Введите данные для удаления: ")
        if file_id.isdigit():
            delete_data_from_file(int(file_id), remove)
        else:
            print("Ошибка! Введите число")

if __name__ == "__main__":
    main()