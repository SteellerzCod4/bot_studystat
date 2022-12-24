from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bot.config_data import ConfigData


engine = create_engine(ConfigData.DB_URI)
Base = declarative_base()

session_maker = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class DBHolder:
    """Контекст обращения к бд (если бд нет, то создать; если есть, то вернуть ссылку на нее)"""

    def __init__(self):
        self.db = session_maker()

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

    def get_bd(self):
        return self.db


def get_db():
    """Функция для получения текущей сессии к БД"""
    return db_holder.get_bd()


db_holder = DBHolder()
