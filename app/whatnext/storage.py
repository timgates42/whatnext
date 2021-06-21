"""
Record whatnext details to avoid reprocessing
"""

from sqlalchemy import Column, String, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql:///whatnext")
Base = declarative_base()
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


# pylint: disable=too-few-public-methods
class Repository(Base):
    """
    Record details of a target repository
    """
    __tablename__ = "repository"
    orgrepo = Column(String, primary_key=True)


def check_db():
    """
    Connect to the database
    """
    try:
        with engine.connect():
            pass
    except OperationalError as err:
        raise Exception("Please setup access to postgres whatnext db") from err
    Base.metadata.create_all(engine)

def connect_db():
    """
    Return a db session
    """
    check_db()
    session = DBSession()
    return session

if __name__ == "__main__":
    check_db()
