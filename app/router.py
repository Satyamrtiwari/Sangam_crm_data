from app.table_metadata import TABLE_DESCRIPTIONS
import re


def get_relevant_tables(question):

    question = question.lower()

    words = set(
        re.findall(
            r'\w+',
            question
        )
    )

    scores = {}

    for table,desc in TABLE_DESCRIPTIONS.items():

        desc_words = set(
            re.findall(
                r'\w+',
                desc.lower()
            )
        )

        score = len(
            words.intersection(
                desc_words
            )
        )

        scores[
            table
        ] = score


    sorted_tables = sorted(

        scores.items(),

        key=lambda x:x[1],

        reverse=True

    )


    selected=[]

    for table,score in sorted_tables:

        if score>0:

            selected.append(
                table
            )


    if not selected:

        selected=[
            "users",
            "accounts",
            "leads",
            "opportunities"
        ]


    print(
        "\nTable scores:",
        scores
    )

    print(
        "\nChosen tables:",
        selected
    )

    return selected