from sqlalchemy import create_engine, Column, Integer, String, Boolean
from .security import config
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(config.settings.DATABASE_URL)
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()