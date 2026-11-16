
import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

categories = [
    "Technical Issue",
    "Billing",
    "Account Issue",
    "General Inquiry"
]

headings = {
    "Technical Issue": [
        "Login Problem",
        "Website Error",
        "Application Not Working"
    ],
    "Billing": [
        "Payment Problem",
        "Refund Request",
        "Invoice Issue"
    ],
    "Account Issue": [
        "Password Reset",
        "Account Locked",
        "Profile Update"
    ],
    "General Inquiry": [
        "Service Information",
        "Product Details",
        "General Question"
    ]
}

queries = []

for i in range(1, 101):

    category = random.choice(categories)
    status = random.choice(["Open", "Closed"])

    created_time = datetime.now() - timedelta(
        days=random.randint(1, 60),
        hours=random.randint(1, 23)
    )

    if status == "Closed":
        closed_time = created_time + timedelta(
            hours=random.randint(1, 72)
        )
    else:
        closed_time = None

    queries.append({
        "query_id": i,
        "mail_id": f"client{i}@gmail.com",
        "mobile_number": f"98765{random.randint(10000, 99999)}",
        "query_heading": random.choice(headings[category]),
        "query_description": f"Sample {category} query number {i}",
        "status": status,
        "query_created_time": created_time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "query_closed_time": (
            closed_time.strftime("%Y-%m-%d %H:%M:%S")
            if closed_time else None
        ),
        "category": category
    })

df = pd.DataFrame(queries)

df.to_csv(
    "data/synthetic_client_queries.csv",
    index=False
)

print("Dataset created successfully!")
print("Total records:", len(df))
print(df.head())
