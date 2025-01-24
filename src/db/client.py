from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from db.functions import _functions
from db.tables import Base
from db.config import (
    POSTGRES_DATABASE_URL,
)

DATABASE_URL = POSTGRES_DATABASE_URL

# Create an engine
engine = create_engine(DATABASE_URL)

# Create functions
with engine.connect() as connection:
    for function in _functions:
        connection.execute(text(function.strip()))
    connection.commit()


# Create all tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
