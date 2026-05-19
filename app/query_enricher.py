SYNONYMS = {

    "business":
    "sales revenue deals amount opportunities earnings",

    "sales":
    "revenue deals amount closed won",

    "talked":
    "calls conversations phone discussions",

    "performing":
    "performance productivity sales activities",

    "salesperson":
    "employee user sales executive staff",

    "complaints":
    "tickets issues support problems",

    "payments":
    "invoice money transaction payment_details",

    "contracts":
    "agreement AMC renewals",

    "lead":
    "prospect enquiry customer",

    "customer":
    "account company client"

}


CRM_ENTITIES = {

    "cities":[
        "Mumbai",
        "Delhi",
        "Hyderabad",
        "Pune",
        "Chennai",
        "Surat",
        "Ahmedabad",
        "Kochi",
        "Bangalore"
    ],

    "sources":[
        "IndiaMART",
        "LinkedIn",
        "Website",
        "Referral",
        "JustDial"
    ],

    "sales_stages":[
        "Closed Won",
        "Closed Lost",
        "Negotiation",
        "Proposal"
    ]
}


def enrich_question(
    question
):

    q = question.lower()

    expanded=[]

    words=q.split()


    for word in words:

        expanded.append(
            word
        )


        clean_word=word.strip(
            "?,."
        )


        if clean_word in SYNONYMS:

            expanded.extend(

                SYNONYMS[
                    clean_word
                ].split()

            )


    enriched=" ".join(
        expanded
    )


    detected=[]


    for city in CRM_ENTITIES["cities"]:

        if city.lower() in q:

            detected.append(
                f"city:{city}"
            )


    for source in CRM_ENTITIES["sources"]:

        if source.lower() in q:

            detected.append(
                f"source:{source}"
            )


    if detected:

        enriched += (

            " " +

            " ".join(
                detected
            )

        )


    return enriched