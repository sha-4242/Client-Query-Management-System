
import pandas as pd
import sqlite3

# Read CSV dataset
df = pd.read_csv("data/synthetic_client_queries.csv")

print("Original records:", len(df))

# 1. Remove duplicate records
df = df.drop_duplicates()

# 2. Clean text columns
text_columns = [
    "mail_id",
    "mobile_number",
    "query_heading",
    "query_description",
    "category"
]

for column in text_columns:
    df[column] = df[column].fillna("").astype(str).str.strip()

# 3. Clean status values
df["status"] = df["status"].str.title()

df = df[df["status"].isin(["Open", "Closed"])]

# 4. Fill missing categories
df["category"] = df["category"].replace("", "General Inquiry")

# 5. Clean date columns
df["query_created_time"] = pd.to_datetime(
    df["query_created_time"], errors="coerce"
)

df["query_closed_time"] = pd.to_datetime(
    df["query_closed_time"], errors="coerce"
)

# Remove records without valid creation dates
df = df.dropna(subset=["query_created_time"])

# Open queries must not have closing dates
df.loc[df["status"] == "Open", "query_closed_time"] = None

# Closed queries must have closing dates
df = df[
    (df["status"] == "Open") |
    (df["query_closed_time"].notna())
]

# 6. Connect to SQLite database
conn = sqlite3.connect("database/client_queries.db")
cursor = conn.cursor()

# 7. Insert cleaned records
inserted = 0

for _, row in df.iterrows():

    cursor.execute("""
        SELECT query_id FROM queries
        WHERE mail_id = ?
        AND query_heading = ?
        AND query_created_time = ?
    """, (
        row["mail_id"],
        row["query_heading"],
        row["query_created_time"].strftime("%Y-%m-%d %H:%M:%S")
    ))

    if cursor.fetchone() is None:

        cursor.execute("""
            INSERT INTO queries (
                mail_id,
                mobile_number,
                query_heading,
                query_description,
                status,
                query_created_time,
                query_closed_time,
                category
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["mail_id"],
            row["mobile_number"],
            row["query_heading"],
            row["query_description"],
            row["status"],
            row["query_created_time"].strftime("%Y-%m-%d %H:%M:%S"),
            row["query_closed_time"].strftime("%Y-%m-%d %H:%M:%S")
            if pd.notna(row["query_closed_time"]) else None,
            row["category"]
        ))

        inserted += 1

conn.commit()
conn.close()

print("Dataset cleaning completed!")
print("Cleaned records:", len(df))
print("New records imported:", inserted)
