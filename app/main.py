from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool

from app.agent import agent
from app.llm import llm
from app.schemas import (
    ChatRequest,
    ChatResponse
)

app=FastAPI(
    title="Sangam CRM AI"
)


@app.post(
    "/ask",
    response_model=ChatResponse
)

async def ask(
    request:ChatRequest
):

    try:

        question=request.question

        response=await run_in_threadpool(

            agent.invoke,

            question

        )

        sales=response["output"]

        prompt=f"""

User asked:

{question}

Database result:

{sales}

Create short CRM business response.

2 lines maximum.
"""

        final=await run_in_threadpool(

            llm.invoke,

            prompt

        )

        return {

            "answer":
            final.content

        }

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )