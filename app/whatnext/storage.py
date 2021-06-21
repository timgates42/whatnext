"""
Record whatnext details to avoid reprocessing
"""

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError


def check_db():
    """
    Connect to the database
    """
    try:
        engine = create_engine("postgresql:///whatnext")
        with engine.connect():
            pass
    except OperationalError as err:
        raise Exception("Please setup access to postgres whatnext db") from err


if __name__ == "__main__":
    check_db()
