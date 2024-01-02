from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.settings import SQLALCHEMY_DATABASE_URL


def get_db_context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

MetaData().create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
