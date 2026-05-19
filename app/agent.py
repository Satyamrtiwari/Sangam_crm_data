import os

from dotenv import load_dotenv
from urllib.parse import quote_plus

from sqlalchemy import create_engine

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

from app.llm import llm
from app.business_rules import RULES
from app.router import get_relevant_tables

load_dotenv()

DB_USER = os.getenv(
    "DB_USER"
)

DB_PASSWORD = quote_plus(
    os.getenv(
        "DB_PASSWORD"
    )
)

DB_HOST = os.getenv(
    "DB_HOST"
)

DB_NAME = os.getenv(
    "DB_NAME"
)


DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:"
    f"{DB_PASSWORD}@"
    f"{DB_HOST}:3306/"
    f"{DB_NAME}"
)


engine = create_engine(
    DATABASE_URL
)


def get_agent(question):

    tables = get_relevant_tables(
        question
    )

    print(
        "\nUsing tables:",
        tables
    )

    db = SQLDatabase(
        engine,
        include_tables=tables,
        sample_rows_in_table_info=0
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        prefix=RULES,
        verbose=False,
        top_k=3
    )

    return agent