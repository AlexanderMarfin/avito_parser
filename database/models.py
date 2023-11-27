import datetime
from database.main import Database
from sqlalchemy import Column, INTEGER, VARCHAR, DATE, ForeignKey
from sqlalchemy.orm import relationship


class User(Database.BASE):  # Пользователи
    __tablename__ = "users"
    # Telegram user id
    id = Column(
        INTEGER, unique=True, nullable=False, autoincrement=False, primary_key=True
    )
    # Telegram username
    username = Column(VARCHAR(32), unique=False, nullable=True)
    # Telegram user registration date
    reg_date = Column(DATE, default=datetime.date.today())
    # Last update date
    upd_date = Column(
        DATE, default=datetime.date.today(), onupdate=datetime.date.today()
    )
    # Payment
    payment = relationship(
        "Payment", uselist=False, backref="users", passive_deletes=True
    )


class Session(Database.BASE):  # Сессии
    __tablename__ = "sessions"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    string = Column(VARCHAR(32), nullable=False)
    enable = Column(INTEGER, default=0)


class Payment(Database.BASE):   # Платежи
    __tablename__ = "payments"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    key = Column(VARCHAR(16), unique=True)


class Files(Database.BASE):  # Файлы
    __tablename__ = "files"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    file_link = Column(VARCHAR(32), unique=False, nullable=True)
    date = Column(DATE, onupdate=datetime.date.today())
    flag = Column(VARCHAR(16))


def register_models():
    Database.BASE.metadata.create_all(Database().engine)
