import os
from dotenv import load_dotenv


load_dotenv()


def get_connection_string():
    engine = os.environ.get("DB_ENGINE")
    host = os.environ.get("DB_HOST")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    dbname = os.environ.get("DB_NAME")
    return f"{engine}://{username}:{password}@{host}/{dbname}"


SQLALCHEMY_DATABASE_URL = get_connection_string()
