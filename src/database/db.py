from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    """
    The get_db function is a context manager that returns the database session.
    It also ensures that the connection to the database is closed after each request.

    :return: A database session
    :doc-author: OSA
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
