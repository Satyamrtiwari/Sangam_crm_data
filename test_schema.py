import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()


# Step 1:
# get all tables automatically

cursor.execute(
    "SHOW TABLES"
)

tables_data = cursor.fetchall()


table_names = []

for row in tables_data:

    table_name = list(
        row.values()
    )[0]

    table_names.append(
        table_name
    )


print("\nFound Tables:\n")

for t in table_names:

    print(t)


print("\n"+"="*50)


schema_docs = []


# Step 2:
# describe every table

for table in table_names:

    cursor.execute(
        f"DESCRIBE {table}"
    )

    columns = cursor.fetchall()

    column_names = []

    for c in columns:

        column_names.append(
            c["Field"]
        )


    doc = f"""
Table: {table}

Columns:

{", ".join(column_names)}

"""


    schema_docs.append(doc)


print("\nGenerated Schema Docs:\n")


for d in schema_docs:

    print(d)

    print(
        "-"*50
    )


conn.close()