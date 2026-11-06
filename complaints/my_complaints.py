
import streamlit as st
from pathlib import Path

from complaints.complaint_service import fetch_user_complaints


def show_my_complaints(user_id):

    st.title("My Complaints")

    st.write(
        "View and track the complaints you have submitted."
    )

    if not user_id:
        st.warning("Please log in to view your complaints.")
        return

    complaints = fetch_user_complaints(user_id)

    if not complaints:
        st.info("You have not submitted any complaints yet.")
        return

    st.write(f"Total complaints submitted: {len(complaints)}")

    for complaint in complaints:

        with st.container(border=True):

            st.subheader(
                f"Complaint #{complaint['id']} - {complaint['title']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write("**Category:**", complaint["category"])
                st.write("**Location:**", complaint["location"])

            with col2:
                st.write("**Status:**", complaint["status"])
                st.write("**Date:**", complaint["created_at"])

            st.write("**Description:**")
            st.write(complaint["description"])

            if complaint["image"]:
                image_path = Path(complaint["image"])

                if image_path.exists():
                    st.image(
                        str(image_path),
                        caption="Uploaded Problem Photograph",
                        width=300
                    )

            if complaint["admin_remarks"]:
                st.info(
                    f"Admin Remarks: {complaint['admin_remarks']}"
                )

            st.divider()
