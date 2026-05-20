import os
import pymysql

from dotenv import load_dotenv

load_dotenv()


conn=pymysql.connect(

    host=os.getenv("DB_HOST"),

    user=os.getenv("DB_USER"),

    password=os.getenv("DB_PASSWORD"),

    database=os.getenv("DB_NAME"),

    cursorclass=pymysql.cursors.DictCursor
)



def get_schema_for_tables(
    tables
):


    cursor=conn.cursor()

    docs=[]


    for table in tables:

        cursor.execute(
            f"DESCRIBE {table}"
        )

        cols=cursor.fetchall()


        text=f"\nTable: {table}\n"


        for c in cols:

            field=c["Field"]

            dtype=c["Type"]


            text += (
                f"\nColumn: {field}"
                f"\nType:{dtype}"
            )


            if any(
                x in dtype.lower()
                for x in
                [
                    "varchar",
                    "text"
                ]
            ):

                try:

                    cursor.execute(
f"""
SELECT DISTINCT {field}
FROM {table}
WHERE {field} IS NOT NULL
LIMIT 5
"""
                    )

                    values=cursor.fetchall()


                    vals=[]

                    for v in values:

                        val=v[field]

                        if val:

                            vals.append(
                                str(val)
                            )


                    if vals:

                        text += (

                            "\nExamples:\n"

                            +

                            ",".join(
                                vals
                            )

                        )


                except:

                    pass


            text+="\n"


        docs.append(
            text
        )


    return "\n".join(
        docs
    )