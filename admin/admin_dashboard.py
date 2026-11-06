
import streamlit as st
from pathlib import Path

from complaints.complaint_service import (
    fetch_all_complaints,
    change_complaint_status
)


def show_admin_dashboard():

    st.title("Admin Dashboard")
    st.write("Manage and resolve community complaints.")

    complaints = fetch_all_complaints()

    if not complaints:
        st.info("No complaints have been submitted yet.")
        return

    st.subheader("All Reported Complaints")

    for complaint in complaints:

        with st.container(border=True):

            st.subheader(
                f"#{complaint['id']} - {complaint['title']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Category:**", complaint["category"])
                st.write("**Location:**", complaint["location"])
                st.write("**Status:**", complaint["status"])

            with col2:
                st.write("**Citizen ID:**", complaint["user_id"])
                st.write("**Date:**", complaint["created_at"])

            st.write("**Description:**")
            st.write(complaint["description"])

            if complaint["image"]:
                image_path = Path(complaint["image"])

                if image_path.exists():
                    st.image(str(image_path), width=300)

            st.divider()

            with st.form(f"update_{complaint['id']}"):

                new_status = st.selectbox(
                    "Update Complaint Status",
                    ["Pending", "In Progress", "Resolved", "Rejected"],
                    index=[
                        "Pending",
                        "In Progress",
                        "Resolved",
                        "Rejected"
                    ].index(complaint["status"])
                )

                remarks = st.text_area(
                    "Admin Remarks",
                    value=complaint["admin_remarks"] or ""
                )

                update = st.form_submit_button("Update Complaint")

                if update:
                    try:
                        change_complaint_status(
                            complaint["id"],
                            new_status,
                            remarks
                        )

                        st.success("Complaint updated successfully!")
                        st.rerun()

                    except Exception as error:
                        st.error(f"Update failed: {error}")
