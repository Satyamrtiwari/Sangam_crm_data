FORBIDDEN=[

"DELETE",
"DROP",
"UPDATE",
"INSERT",
"ALTER",
"TRUNCATE",
"CREATE"

]

def validate(sql:str):

    sql=sql.upper()

    for word in FORBIDDEN:

        if word in sql:

            raise Exception(
                f"Blocked SQL: {word}"
            )

    if not sql.startswith(
        "SELECT"
    ):

        raise Exception(
            "Only SELECT allowed"
        )

    return True