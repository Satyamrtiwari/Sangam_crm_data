from sqlalchemy import text

from app.agent import engine

from app.sql_safety import (
    validate_sql
)



def execute_query(
    sql
):

    validate_sql(
        sql
    )


    with engine.connect() as conn:

        result=conn.execute(
            text(sql)
        )


        rows=result.fetchall()


    return rows