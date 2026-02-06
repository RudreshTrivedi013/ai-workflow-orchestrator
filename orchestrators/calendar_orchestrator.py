import re
from datetime import datetime, timedelta

def calendar_orchestrator(user_input: str) -> dict:
    text = user_input.lower()

    # Title
    title = "Meeting"
    if "team" in text:
        title = "Team Meeting"
    if "sync" in text:
        title = "Team Sync"

    # Date
    date = None
    if "tomorrow" in text:
        date = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    # Time
    time = None
    match = re.search(r'(\d{1,2})(am|pm)', text)
    if match:
        hour = int(match.group(1))
        meridian = match.group(2)
        if meridian == "pm" and hour != 12:
            hour += 12
        time = f"{hour:02d}:00"

    # Platform
    location = None
    if "google meet" in text:
        location = "Google Meet"
    elif "zoom" in text:
        location = "Zoom"

    return {
        "title": title,
        "date": date,
        "time": time,
        "timezone": "IST",
        "location": location,
        "participants": ["You"],
        "description": user_input
    }
