from app.agent import get_agent
from app.llm import llm


question = "show total sales in Hyderabad"

agent = get_agent(
    question
)

response = agent.invoke(
    question
)

sales = response["output"]

print(
    "\nAgent output:"
)

print(
    sales
)

prompt = f"""
You are Sangam CRM assistant.

Rules:

1. Currency always ₹ INR

2. Never invent trends

3. Never hallucinate

Question:
{question}

Database result:
{sales}

Generate answer in 2 lines.
"""

final = llm.invoke(
    prompt
)

print(
    "\nBot response:"
)

print(
    final.content
)