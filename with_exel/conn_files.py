from connection import DB_PARAMS
import psycopg2
import os

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
        print(f"✅ Файл {file_path} загружен в базу!")
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    finally:
        cursor.close()
        conn.close()

def download_file(file_id):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM files WHERE id = %s", (file_id,))
        row = cursor.fetchone()
        
        if row:
            cursor.execute("DELETE FROM files WHERE id = %s", (file_id,))
            conn.commit()
            print(f"🗑️ Файл с ID {file_id} успешно удалён из базы данных.")
        else:
            print("❌ Файл с таким ID не найден.")
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    finally:
        cursor.close()
        conn.close()

def update_file(file_id, new_data):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute("SELECT filedata FROM files WHERE id = %s", (file_id,))
        row = cursor.fetchone()
        if row:
            existing_data = bytes(row[0])
            updated_data = existing_data + new_data.encode()  
            
            cursor.execute("UPDATE files SET filedata = %s WHERE id = %s", (updated_data, file_id))
            conn.commit()
            print(f"✅ Данные добавлены в файл с ID {file_id}!")
        else:
            print("❌ Файл с таким ID не найден.")
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    finally:
        cursor.close()
        conn.close()


def delete_data_from_file(file_id, data_to_remove):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cursor = conn.cursor()
        cursor.execute("SELECT filedata FROM files WHERE id = %s", (file_id,))
        row = cursor.fetchone()
        
        if row:
            existing_data = bytes(row[0])
            updated_data = existing_data.replace(data_to_remove.encode(), b"")
            
            cursor.execute("UPDATE files SET filedata = %s WHERE id = %s", (updated_data, file_id))
            conn.commit()
            print(f"✅ Данные удалены из файла с ID {file_id}!")
        else:
            print("❌ Файл с таким ID не найден.")
    except psycopg2.Error as e:
        print(f"❌ Ошибка базы данных: {e}")
    finally:
        cursor.close()
        conn.close()
