from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from src.conf.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
URI = SQLALCHEMY_DATABASE_URL
engine = create_engine(URI, echo=True)

DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency
def get_db():
    """
    The get_db function is a context manager that will automatically close the database session at the end of a request.
    It also handles any exceptions that occur during the request, rolling back any changes to the database if an exception occurs.

    :return: A database connection from the pool
    """
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
