from app.agent import agent
from app.llm import llm

question="how much bussinees i made in this month in kochi"

response=agent.invoke(question)

sales=response["output"]

print(
"\nAgent output:"
)

print(sales)

prompt=f"""

User asked:

{question}

Database result:

{sales}

Create short CRM business summary.

Example:

Mumbai sales: ₹21,627,221

Sales performance looks strong.

Only 2 lines.
"""

final=llm.invoke(
prompt
)

print(
"\nBot response:"
)

print(
final.content
)