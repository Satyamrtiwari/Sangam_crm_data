from app.retriever import (
    get_relevant_tables
)


tests=[

"show total sales in Mumbai",

"show people i talked to",

"which salesperson has most leads",

"how much business i made this month",

"how is Ravi performing"

]


for t in tests:

    print("\n"+"="*50)

    print(
        "\nQUESTION:"
    )

    print(t)

    get_relevant_tables(
        t
    )