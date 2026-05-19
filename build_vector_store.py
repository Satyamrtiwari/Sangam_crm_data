import os
import pymysql
from dotenv import load_dotenv
import chromadb

from langchain_mistralai import MistralAIEmbeddings

load_dotenv()


embedder = MistralAIEmbeddings(
    model="mistral-embed",
    api_key=os.getenv(
        "MISTRAL_API_KEY"
    )
)


client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = client.get_or_create_collection(
    name="sangam_schema"
)


conn = pymysql.connect(

    host=os.getenv("DB_HOST"),

    user=os.getenv("DB_USER"),

    password=os.getenv("DB_PASSWORD"),

    database=os.getenv("DB_NAME"),

    cursorclass=pymysql.cursors.DictCursor
)


cursor=conn.cursor()


BUSINESS_HINTS={

"users":"""
Stores CRM employees and salespeople.

Use for:

employee performance
salesperson performance
team member performance
who closed deals
assigned opportunities
assigned leads
sales metrics
Ravi Priya employee questions

Related tables:

opportunities
activities
calls
leads

Common words:

employee
salesperson
performance
team
staff
manager
""",

"accounts":"""
Stores customer companies.

Use for:

customer information
industry analysis
organizations
client companies

Related tables:

users

Common words:

customer
client
company
organization
industry
""",

"leads":"""
Stores enquiries and prospects.

Use for:

lead source
IndiaMART leads
JustDial leads
prospects
potential customers
lead conversion

Related tables:

users
opportunities

Common words:

enquiry
prospect
lead
source
customer
""",


"opportunities":"""
Stores sales opportunities and deal information.

Use for:

sales totals
revenue
business generated
Mumbai sales
monthly sales
deal amount
highest sales
closed won
closed lost
sales performance

Related tables:

users

Common words:

sales
revenue
deal
business
earning
profit
amount
closed
""",


"tickets":"""
Stores support complaints.

Use for:

complaints
customer support
issues
resolved tickets
priority tickets

Related tables:

users
accounts

Common words:

complaint
support
issue
problem
ticket
""",


"contracts":"""
Stores agreements and AMC contracts.

Use for:

active contracts
renewals
expiring contracts
agreement values

Related tables:

accounts

Common words:

contract
AMC
renewal
agreement
""",


"payment_details":"""
Stores payment information.

Use for:

pending payments
overdue payments
received money
payment tracking
invoice tracking

Related tables:

users
accounts

Common words:

payment
invoice
money
pending
received
transaction
""",


"activities":"""
Stores meetings and followups.

Use for:

activity history
customer interactions
followups
meeting history
salesperson activity

Related tables:

users
accounts

Common words:

meeting
activity
interaction
history
followup
""",


"calls":"""
Stores phone conversations.

Use for:

people i talked to
call history
customer discussions
phone activity
call outcomes

Related tables:

users
accounts

Common words:

call
talked
conversation
phone
discussion
speak
"""
}


cursor.execute(
"SHOW TABLES"
)

tables=cursor.fetchall()


for row in tables:

    table=list(
        row.values()
    )[0]


    cursor.execute(
        f"DESCRIBE {table}"
    )


    cols=cursor.fetchall()


    col_names=[]


    for c in cols:

        col_names.append(
            c["Field"]
        )


    schema_doc=f"""

Table Name:

{table}

Database Purpose:

{BUSINESS_HINTS.get(table,"")}

Columns:

{",".join(col_names)}

Relationships:

users.id ← leads.assigned_user_id

users.id ← opportunities.assigned_user_id

users.id ← tickets.assigned_user_id

users.id ← payment_details.assigned_user_id

users.id ← calls.assigned_user_id

accounts.id ← activities.account_id

Business Meaning:

Users manage leads,
users close opportunities,
users make calls,
users perform activities,
users handle tickets.

Sales come from opportunities.amount
with sales_stage='Closed Won'

Payments come from payment_details

Calls represent customer discussions

"""




    vector=embedder.embed_query(
        schema_doc
    )


    collection.add(

        ids=[table],

        embeddings=[vector],

        documents=[schema_doc]

    )


    print(
        f"Stored {table}"
    )


print(
"\nDONE"
)

conn.close()