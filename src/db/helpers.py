"""
These SQLAlchemy helpers are used to convert queries to DataFrames and SQL strings.
"""

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm.decl_api import DeclarativeMeta

from db import session, text
from analysis import *


def query_to_df(query):
    # Execute the query and get the result proxy
    result_proxy = query.execution_options(stream_results=True)

    # Get the column names
    col_names = [col["name"] for col in result_proxy.column_descriptions]

    # Fetch all data
    data = result_proxy.all()

    # Return empty data
    if len(data) == 0:
        return None

    # Check if we're working with a table
    if isinstance(result_proxy.column_descriptions[0]["type"], DeclarativeMeta):
        # Rewrite col names to be the table columns
        col_names = data[0].__table__.columns.keys()
        # Fetch data correctly
        data = [
            {key: getattr(item, key) for key in item.__table__.columns.keys()}
            for item in data
        ]

    # Create a DataFrame
    df = pd.DataFrame(data, columns=col_names)

    # Set id to index if it exists
    if "id" in df.columns:
        df.set_index("id", inplace=True)

    return df


def to_sql(query):
    return str(
        query.statement.compile(
            dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}
        )
    )


def from_sql(query):
    return text(query)
