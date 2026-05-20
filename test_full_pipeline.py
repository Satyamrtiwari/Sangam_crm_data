from app.agent import (
    get_agent
)


question="show total sales in Mumbai"


agent=get_agent(
    question
)


response=agent.invoke(
    question
)


print(
    "\nAgent Output:\n"
)

print(
    response["output"]
)