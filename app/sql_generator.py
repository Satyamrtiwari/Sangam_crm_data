from app.llm import llm

from app.retriever import (
    get_relevant_tables
)

from app.schema_loader import (
    get_schema_for_tables
)

from app.business_rules import (
    RULES
)



def generate_sql(
    question
):


    tables=get_relevant_tables(
        question
    )


    schema=(
        get_schema_for_tables(
            tables
        )
    )


    prompt=f"""

You are CRM SQL expert.

{RULES}

Available schema:

{schema}


Question:

{question}


Generate SQL only.

No markdown.

"""


    response=llm.invoke(
        prompt
    )


    sql=response.content.strip()


    return sql