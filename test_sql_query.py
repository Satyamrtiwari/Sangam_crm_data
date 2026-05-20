from app.sql_generator import (
    generate_sql
)

from app.query_executor import (
    execute_query
)


QUESTIONS=[

"What is the highest sales and in which city"
]


for question in QUESTIONS:

    print("\n"+"="*70)

    print(
        "\nQUESTION:"
    )

    print(
        question
    )


    try:

        sql=generate_sql(
            question
        )


        print(
            "\nGenerated SQL:\n"
        )

        print(
            sql
        )


        result=execute_query(
            sql
        )


        print(
            "\nResult:\n"
        )

        print(
            result
        )


    except Exception as e:

        print(
            "\nERROR:\n"
        )

        print(e)