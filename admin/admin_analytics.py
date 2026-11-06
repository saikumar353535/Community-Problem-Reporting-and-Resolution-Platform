
import streamlit as st
import pandas as pd
import plotly.express as px

from complaints.complaint_service import (
    fetch_all_complaints,
    get_complaint_statistics
)


def show_admin_analytics():

    st.title("Complaint Analytics")

    complaints = fetch_all_complaints()
    stats = get_complaint_statistics()

    st.subheader("Overall Complaint Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Complaints", stats["total"])
    col2.metric("Pending", stats["pending"])
    col3.metric("In Progress", stats["in_progress"])

    col4, col5 = st.columns(2)

    col4.metric("Resolved", stats["resolved"])
    col5.metric("Rejected", stats["rejected"])

    st.divider()

    if not complaints:
        st.info("No complaint data available for analytics.")
        return

    st.subheader("Complaint Status Distribution")

    status_data = pd.DataFrame({
        "Status": [
            "Pending",
            "In Progress",
            "Resolved",
            "Rejected"
        ],
        "Count": [
            stats["pending"],
            stats["in_progress"],
            stats["resolved"],
            stats["rejected"]
        ]
    })

    fig = px.pie(
        status_data,
        names="Status",
        values="Count",
        title="Complaints by Status",
        hole=0.4
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Complaints by Category")

    category_data = pd.DataFrame([
        dict(complaint)
        for complaint in complaints
    ])

    category_counts = (
        category_data["category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = ["Category", "Count"]

    fig2 = px.bar(
        category_counts,
        x="Category",
        y="Count",
        title="Complaints by Category",
        text="Count"
    )

    st.plotly_chart(fig2, use_container_width=True)
