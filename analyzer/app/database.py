import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()


def get_connection_string():
    db_engine = os.environ.get("DB_ENGINE")
    host = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_DATABASE")
    return f"{db_engine}://{username}:{password}@{host}/{dbname}"


SQLALCHEMY_DB_URL = get_connection_string()

engine = create_engine(SQLALCHEMY_DB_URL)
metadata = MetaData()

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
