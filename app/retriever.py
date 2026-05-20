import os
from dotenv import load_dotenv
import chromadb

from langchain_mistralai import MistralAIEmbeddings

from app.query_enricher import (
    enrich_question
)

load_dotenv()


embedder=MistralAIEmbeddings(

    model="mistral-embed",

    api_key=os.getenv(
        "MISTRAL_API_KEY"
    )

)


client=chromadb.PersistentClient(
    path="./chroma_db"
)


collection=client.get_collection(
    name="sangam_schema"
)



def get_relevant_tables(

    question,

    top_k=9,

    gap_threshold=0.05,

    max_tables=3,

    high_distance_cap=0.75,

    high_distance_max=2
):


    enriched_question=(
        enrich_question(
            question
        )
    )


    vector=embedder.embed_query(
        enriched_question
    )


    result=collection.query(

        query_embeddings=[
            vector
        ],

        n_results=top_k

    )


    ids=result["ids"][0]

    distances=result["distances"][0]


    best_score=distances[0]


    if best_score > high_distance_cap:

        active_gap=0.03

        active_max=high_distance_max

    else:

        active_gap=gap_threshold

        active_max=max_tables


    final_tables=[
        (
            ids[0],
            distances[0]
        )
    ]


    for i in range(
        1,
        len(ids)
    ):


        prev_score=distances[
            i-1
        ]


        curr_score=distances[
            i
        ]


        gap=(
            curr_score-
            prev_score
        )


        if gap > active_gap:

            break


        final_tables.append(

            (
                ids[i],
                curr_score
            )

        )


        if len(
            final_tables
        )>=active_max:

            break


    selected=[

        x[0]

        for x in final_tables

    ]


    print(
        "\nEnriched:",
        enriched_question
    )


    print(
        "\nRetrieved:",
        selected
    )


    return selected