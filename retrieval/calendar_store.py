import sqlite3

conn = sqlite3.connect("calendar.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    time TEXT,
    location TEXT
)
""")
conn.commit()

def save_event(event):
    cursor.execute(
        "INSERT INTO events (title, date, time, location) VALUES (?, ?, ?, ?)",
        (
            event.get("title"),
            event.get("date"),
            event.get("time"),
            event.get("location")
        )
    )
    conn.commit()
