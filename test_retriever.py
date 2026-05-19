import os
from dotenv import load_dotenv
import chromadb

from langchain_mistralai import MistralAIEmbeddings

load_dotenv()


embedder = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv("MISTRAL_API_KEY")
)


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_collection(
    name="sangam_schema"
)


def retrieve_tables(
    question,
    top_k=9,
    gap_threshold=0.05,
    max_tables=3,
    high_distance_cap=0.75,
    high_distance_max=2
):
    """
    Gap-based dynamic retrieval with absolute distance cap.

    Two rules work together:

    Rule 1 — Gap detection:
        If score jumps more than gap_threshold
        between two consecutive results → stop.
        Works great when best score is low (clear match).

    Rule 2 — High distance cap:
        If best score itself is > high_distance_cap,
        the question is ambiguous (no strong match exists).
        In that case, limit to high_distance_max tables max,
        and apply a tighter gap of 0.03.
        Prevents noise when everything looks "kind of similar".

    Args:
        gap_threshold      : normal jump threshold (0.05)
        max_tables         : hard cap on tables returned (3)
        high_distance_cap  : if best score > this -> ambiguous mode
        high_distance_max  : max tables in ambiguous mode (2)
    """

    vector = embedder.embed_query(question)

    result = collection.query(
        query_embeddings=[vector],
        n_results=top_k
    )

    ids       = result["ids"][0]
    distances = result["distances"][0]

    best_score = distances[0]

    # Rule 2: if even best match is weak -> ambiguous question
    # tighten gap and reduce max tables
    if best_score > high_distance_cap:
        active_gap = 0.03
        active_max = high_distance_max
    else:
        active_gap = gap_threshold
        active_max = max_tables

    # always keep first (best match)
    final_tables = [(ids[0], distances[0])]

    for i in range(1, len(ids)):

        prev_score = distances[i - 1]
        curr_score = distances[i]

        gap = curr_score - prev_score

        if gap > active_gap:
            break

        final_tables.append((ids[i], curr_score))

        if len(final_tables) >= active_max:
            break


    print("\n" + "=" * 50)
    print(f"\nQuestion:\n{question}")

    # show mode for debugging
    mode = "AMBIGUOUS" if best_score > high_distance_cap else "NORMAL"
    print(f"Mode: {mode} (best_distance={round(best_score, 4)})")

    print("\nSelected Tables:\n")
    for table, score in final_tables:
        print(f"  {table} | distance={round(score, 4)}")

    return [t[0] for t in final_tables]


# ── Test Suite ──────────────────────────────────────

TESTS = [

    # NORMAL cases - clear single table
    "show total sales in Mumbai",
    "show pending payments",
    "show active contracts",
    "show complaints in Delhi",
    "which leads came from IndiaMART",
    "show overdue payments",
    "show expired contracts",
    "total calls made this week",

    # NORMAL cases - needs 2 tables
    "who closed highest sales",
    "which salesperson has most leads",

    # AMBIGUOUS cases - vague questions
    "how is Ravi performing",
    "how much business i made in this month",
    "how many business i made this week",
    "show people i talked to",

]


for q in TESTS:
    retrieve_tables(q)