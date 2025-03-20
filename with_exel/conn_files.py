from connection import DB_PARAMS
import psycopg2
import os

# Создание таблицы
def create_table():
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                filename TEXT,
                filedata BYTEA
            )
        """)
        conn.commit()
        print("✅ Таблица создана!")
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    finally:
        cursor.close()
        conn.close()

# Функция загрузки файла в базу
def excel_pull(file_path):
    if not os.path.exists(file_path):
        print("❌ Ошибка: Файл не найден.")
        return

    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        with open(file_path, "rb") as file:
            file_data = file.read()
            cursor.execute("INSERT INTO files (filename, filedata) VALUES (%s, %s)", (file_path, file_data))

        conn.commit()
        print(f"✅ Файл {file_path} успешно загружен в базу данных!")
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    finally:
        cursor.close()
        conn.close()

# Функция извлечения файла по ID
def download_file(file_id):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()

        cursor.execute("SELECT filename, filedata FROM files WHERE id = %s", (file_id,))
        row = cursor.fetchone()

        if row:
            filename, file_data = row
            restored_filename = f"restored_{os.path.basename(filename)}"

            with open(restored_filename, "wb") as file:
                file.write(file_data)

            print(f"✅ Файл восстановлен и сохранён как {restored_filename}")
        else:
            print("❌ Файл с таким ID не найден.")
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_table()

    while True:
        print("\n🔹 Выберите действие:")
        print("1 - Загрузить файл")
        print("2 - Извлечь файл")
        print("3 - Выход")
        choice = input("Ваш выбор: ").strip()

        if choice == "1":
            file_path = input("Введите путь к файлу для загрузки: ").strip()
            excel_pull(file_path)
        elif choice == "2":
            file_id = input("Введите ID файла для извлечения: ").strip()
            if file_id.isdigit():
                download_file(int(file_id))
            else:
                print("❌ Ошибка: ID должен быть числом.")
        elif choice == "3":
            print("👋 Выход из программы.")
            break
        else:
            print("❌ Ошибка: Неверный ввод. Попробуйте снова.")