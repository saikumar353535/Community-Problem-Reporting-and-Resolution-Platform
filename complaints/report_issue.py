
import streamlit as st
from pathlib import Path
import uuid

from complaints.complaint_service import submit_complaint


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


def show_report_issue(user_id):

    st.title("Report a Community Problem")

    st.write(
        "Help improve your community by reporting "
        "problems in your area."
    )

    with st.form("complaint_form"):

        title = st.text_input(
            "Complaint Title",
            placeholder="Example: Damaged road near bus stop"
        )

        category = st.selectbox(
            "Select Problem Category",
            [
                "Road Damage",
                "Garbage",
                "Water Leakage",
                "Streetlight",
                "Drainage",
                "Other"
            ]
        )

        description = st.text_area(
            "Describe the Problem",
            placeholder="Explain the problem in detail..."
        )

        location = st.text_input(
            "Problem Location",
            placeholder="Enter area or address"
        )

        uploaded_image = st.file_uploader(
            "Upload Problem Photograph",
            type=["jpg", "jpeg", "png"]
        )

        submitted = st.form_submit_button(
            "Submit Complaint"
        )

        if submitted:

            if not user_id:
                st.error("Please log in before submitting.")
            
            elif not all([
                title.strip(),
                description.strip(),
                location.strip()
            ]):
                st.error("Please fill in all required fields.")

            else:
                image_path = None

                try:
                    if uploaded_image is not None:

                        image_data = uploaded_image.getvalue()

                        if len(image_data) > 5 * 1024 * 1024:
                            st.error("Image must be smaller than 5 MB.")
                            return

                        extension = Path(
                            uploaded_image.name
                        ).suffix.lower()

                        image_name = f"{uuid.uuid4().hex}{extension}"

                        image_path = str(UPLOAD_DIR / image_name)

                        with open(image_path, "wb") as image_file:
                            image_file.write(image_data)

                    complaint_id = submit_complaint(
                        user_id=user_id,
                        title=title,
                        category=category,
                        description=description,
                        location=location,
                        image=image_path
                    )

                    st.success(
                        f"Complaint submitted successfully! "
                        f"Your Complaint ID is #{complaint_id}"
                    )

                    st.info("Current Status: Pending")

                except Exception as error:
                    st.error(f"Could not submit complaint: {error}")
