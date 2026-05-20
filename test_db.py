from database import run_query

query="""
SELECT 
SUM(amount) AS total_sales
FROM opportunities
WHERE city='Mumbai'
AND sales_stage='Closed Won'
AND deleted_at IS NULL
"""

results,error=run_query(query)

print(results)