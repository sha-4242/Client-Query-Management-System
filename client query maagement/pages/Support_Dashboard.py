
import streamlit as st
import pandas as pd
from database.db import create_connection, close_query

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #eef2ff, #f5f3ff);
}

h1 {
    color: #4338ca !important;
    font-weight: 800;
}

h2, h3 {
    color: #4f46e5 !important;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #ddd6fe;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(79, 70, 229, 0.08);
}

.stButton > button {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #3730a3;
    color: white;
    border: none;
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Support Dashboard",
    page_icon="📩",
    layout="wide"
)

st.title("📩 Support Dashboard")
st.write("Manage and monitor client queries.")

# 1. Load Queries
conn = create_connection()
df = pd.read_sql_query("SELECT * FROM queries", conn)
conn.close()

# Convert date columns
if not df.empty:
    df["query_created_time"] = pd.to_datetime(
        df["query_created_time"], errors="coerce"
    )
    df["query_closed_time"] = pd.to_datetime(
        df["query_closed_time"], errors="coerce"
    )

# 2. Query Statistics
st.subheader("Query Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Queries", len(df))

with col2:
    st.metric(
        "Open Queries",
        len(df[df["status"] == "Open"])
    )

with col3:
    st.metric(
        "Closed Queries",
        len(df[df["status"] == "Closed"])
    )

st.divider()

# 3. Manage Client Queries
st.subheader("Manage Client Queries")

col1, col2 = st.columns(2)

with col1:
    status = st.selectbox(
        "Filter by Status",
        ["All", "Open", "Closed"]
    )

with col2:
    categories = ["All"]

    if not df.empty:
        categories += sorted(
            df["category"].dropna().unique().tolist()
        )

    category = st.selectbox(
        "Filter by Category",
        categories
    )

filtered_df = df.copy()

if status != "All":
    filtered_df = filtered_df[
        filtered_df["status"] == status
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == category
    ]

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True)
else:
    st.info("No queries found.")

st.divider()

# 4. Close Query
st.subheader("Close a Query")

open_queries = df[df["status"] == "Open"]

if not open_queries.empty:

    query_id = st.selectbox(
        "Select Query ID",
        open_queries["query_id"].tolist()
    )

    if st.button("Close Query"):
        close_query(query_id)
        st.success("Query closed successfully!")
        st.rerun()

else:
    st.info("No open queries available.")

st.divider()

# 5. Query Status Analytics
st.subheader("Query Status Analytics")

if not df.empty:

    st.bar_chart(df["status"].value_counts())

    st.subheader("Queries by Category")
    st.bar_chart(df["category"].value_counts())

    st.divider()

    # 6. Daily Query Trend Analysis
    st.subheader("Daily Query Trend Analysis")

    daily_queries = (
        df.dropna(subset=["query_created_time"])
        .groupby(df["query_created_time"].dt.date)
        .size()
    )

    if not daily_queries.empty:
        st.line_chart(daily_queries)
    else:
        st.info("No date information available.")

    st.divider()

    # 7. Resolution Time Analysis
    st.subheader("Resolution Time Analysis")

    closed_queries = df[
        (df["status"] == "Closed") &
        (df["query_closed_time"].notna()) &
        (df["query_created_time"].notna())
    ].copy()

    if not closed_queries.empty:

        closed_queries["resolution_hours"] = (
            closed_queries["query_closed_time"] -
            closed_queries["query_created_time"]
        ).dt.total_seconds() / 3600

        average_time = closed_queries[
            "resolution_hours"
        ].mean()

        st.metric(
            "Average Resolution Time",
            f"{average_time:.2f} hours"
        )

        st.subheader("Resolution Time by Query ID")

        st.bar_chart(
            closed_queries.set_index("query_id")[
                "resolution_hours"
            ]
        )

        st.dataframe(
            closed_queries[
                ["query_id", "query_heading", "resolution_hours"]
            ],
            use_container_width=True
        )

    else:
        st.info(
            "No closed queries available for resolution analysis."
        )

    st.divider()

    # 8. Backlog Analysis
    st.subheader("Backlog Analysis")

    open_queries = df[df["status"] == "Open"].copy()

    st.metric("Pending Query Backlog", len(open_queries))

    if not open_queries.empty:

        open_queries["pending_days"] = (
            pd.Timestamp.now() -
            open_queries["query_created_time"]
        ).dt.total_seconds() / 86400

        st.metric(
            "Average Pending Days",
            f"{open_queries['pending_days'].mean():.2f} days"
        )

        st.subheader("Pending Queries by Age")

        st.bar_chart(
            open_queries.set_index("query_id")["pending_days"]
        )

    else:
        st.success("There are no pending queries.")

    st.divider()

    # 9. Support Workload Analysis
    st.subheader("Support Workload Analysis")

    if not open_queries.empty:

        workload = open_queries["category"].value_counts()

        st.bar_chart(workload)

        workload_df = workload.rename_axis(
            "Category"
        ).reset_index(name="Open Query Count")

        st.dataframe(
            workload_df,
            use_container_width=True
        )

    else:
        st.info("No open queries to calculate workload.")

    st.divider()

    # 10. Query Details
    st.subheader("Query Details")

    st.write("Total Queries:", len(df))
    st.write(
        "Open Queries:",
        len(df[df["status"] == "Open"])
    )
    st.write(
        "Closed Queries:",
        len(df[df["status"] == "Closed"])
    )

else:
    st.info("No query data available for analytics.")

# 11. Refresh Dashboard
if st.button("Refresh Dashboard"):
    st.rerun()
