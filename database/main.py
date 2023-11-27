from typing import Final
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from misc import singleton
from config_data.config import Config, load_config

config: Config = load_config()


class Database(metaclass=singleton.SingletonMeta):  # Singleton для создания одного и только одного экземпляра объекта
    BASE: Final = declarative_base()

    def __init__(self) -> None:  # Параметры подключения к БД
        url = (
            "postgresql://"
            + config.db_config.user
            + ":"
            + config.db_config.password
            + "@"
            + config.db_config.host
            + ":"
            + config.db_config.port
            + "/"
            + config.db_config.database
        )
        self.__engine = create_engine(url, echo=True)
        session = sessionmaker(bind=self.__engine)
        self.__session = session()

    @property
    def session(self) -> Session:
        return self.__session

    @property
    def engine(self) -> Engine:
        return self.__engine
