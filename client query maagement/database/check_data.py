import sqlite3

conn = sqlite3.connect("database/client_queries.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM queries")

total = cursor.fetchone()[0]

print("Total queries in database:", total)

cursor.execute("""
    SELECT status, COUNT(*)
    FROM queries
    GROUP BY status
""")

print("\nQuery Status:")
for row in cursor.fetchall():
    print(row)

conn.close()