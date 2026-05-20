import re


FORBIDDEN=[

    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE"

]


def validate_sql(
    query
):


    q=query.upper()


    words=set(

        re.findall(
            r"\b[A-Z_]+\b",
            q
        )

    )


    for word in FORBIDDEN:

        if word in words:

            raise Exception(

                f"Blocked SQL: {word}"

            )


    if not q.strip().startswith(
        "SELECT"
    ):

        raise Exception(
            "Only SELECT allowed"
        )


    return True