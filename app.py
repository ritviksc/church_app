from flask import Flask,render_template,request,jsonify
import sqlite3

app = Flask(__name__)

# Databases for required sections
def init_db():
    conn = sqlite3.connect("church.db")
    cursor = conn.cursor()

    # Events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        location TEXT NOT NULL,
        capacity INTEGER NOT NULL
    )
    """)
    
     # Check if events table is empty
    cursor.execute("SELECT COUNT(*) FROM events")
    count = cursor.fetchone()[0]

    # Some dummy data for testing
    if count == 0:
        cursor.execute("""
            INSERT INTO events (title, description, date, location, capacity)
            VALUES (?, ?, ?, ?, ?)
        """, ("Sunday Service", "Morning worship gathering", "2026-03-01", "Main Hall", 100))

        cursor.execute("""
            INSERT INTO events (title, description, date, location, capacity)
            VALUES (?, ?, ?, ?, ?)
        """, ("Youth Night", "Games and discussion for youth", "2026-03-05", "Youth Room", 40))

        cursor.execute("""
            INSERT INTO events (title, description, date, location, capacity)
            VALUES (?, ?, ?, ?, ?)
        """, ("Community Outreach", "Helping the local community", "2026-03-10", "Downtown Center", 2))

    conn.commit()
    conn.close()

@app.route("/")
@app.route("/home")
def church_app():
    return render_template("home.html")

@app.route("/about")
def about():
    return "This is the church management system backend"


@app.route("/events")
def events_page():
    conn = sqlite3.connect("church.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM events")
    rows = cursor.fetchall()

    conn.close()

    events = []
    for row in rows:
        events.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "date": row[3],
            "location": row[4],
            "capacity": row[5]
        })

    return render_template("events.html", events=events)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
