# Задача "Модели SQLAlchemy":
# База данных и движок:


from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

engine = create_engine('sqlite:///taskmanager.db', echo=True)

SessionLocal = sessionmaker(bind=engine)
session = Session()

class Base(DeclarativeBase):
    pass
