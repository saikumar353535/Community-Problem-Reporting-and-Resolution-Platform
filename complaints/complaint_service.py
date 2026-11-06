
from database import (
    add_complaint,
    get_user_complaints,
    get_all_complaints,
    update_complaint_status
)

VALID_STATUSES = [
    "Pending",
    "In Progress",
    "Resolved",
    "Rejected"
]


def submit_complaint(
    user_id,
    title,
    category,
    description,
    location,
    image=None
):
    """Submit a new community complaint."""

    if not all([
        user_id,
        title.strip(),
        category.strip(),
        description.strip(),
        location.strip()
    ]):
        raise ValueError("Please fill in all required fields.")

    complaint_id = add_complaint(
        user_id,
        title.strip(),
        category.strip(),
        description.strip(),
        location.strip(),
        image
    )

    return complaint_id


def fetch_user_complaints(user_id):
    """Get complaints submitted by a particular citizen."""

    return get_user_complaints(user_id)


def fetch_all_complaints():
    """Get all complaints for the admin dashboard."""

    return get_all_complaints()


def change_complaint_status(complaint_id, status, remarks=""):
    """Update complaint status by admin."""

    if status not in VALID_STATUSES:
        raise ValueError("Invalid complaint status.")

    if not complaint_id:
        raise ValueError("Invalid complaint ID.")

    update_complaint_status(
        complaint_id,
        status,
        remarks.strip()
    )

    return True


def get_complaint_statistics():
    """Calculate complaint statistics."""

    complaints = fetch_all_complaints()

    total = len(complaints)

    pending = sum(
        1 for c in complaints if c["status"] == "Pending"
    )

    in_progress = sum(
        1 for c in complaints if c["status"] == "In Progress"
    )

    resolved = sum(
        1 for c in complaints if c["status"] == "Resolved"
    )

    rejected = sum(
        1 for c in complaints if c["status"] == "Rejected"
    )

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "rejected": rejected
    }
