from app.query_enricher import (
    enrich_question
)


tests=[

"how much business i made this month",

"show people i talked to",

"which salesperson has most leads",

"show total sales in Mumbai",

"how is Ravi performing"

]


for t in tests:

    print("\n"+"="*50)

    print(
        "Original:"
    )

    print(t)

    print(
        "\nEnriched:"
    )

    print(
        enrich_question(t)
    )