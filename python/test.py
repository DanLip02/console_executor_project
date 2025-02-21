from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String

# Подключение к базе данных
engine = create_engine("sqlite:///database.db", echo=True)
metadata = MetaData()

# Определение таблицы
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('age', Integer))

# Создание таблицы в базе данных
metadata.create_all(engine)

# Вставка данных
with engine.connect() as connection:
    connection.execute(users.insert(), [{"name": "Иван", "age": 25}, {"name": "Мария", "age": 30}])

# Запрос данных
with engine.connect() as connection:
    result = connection.execute(users.select())
    for row in result:
        print(row)