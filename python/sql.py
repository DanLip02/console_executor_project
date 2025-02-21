from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Подключение к базе данных
engine = create_engine("sqlite:///database.db", echo=True)
Base = declarative_base()

# Определение таблицы
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, age={self.age})"

# Создание таблицы
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Добавление пользователей
user1 = User(name="Иван", age=25)
user2 = User(name="Мария", age=30)
session.add_all([user1, user2])
session.commit()

# Вывод всех пользователей
users = session.query(User).all()
for user in users:
    print(user)

# Закрытие сессии
session.close()
