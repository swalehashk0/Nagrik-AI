import sqlite3


def create_database():
    conn = sqlite3.connect("nagrik_ai.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT,
            role TEXT DEFAULT 'citizen'
        )
    """)

    # Complaints table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            citizen_name TEXT NOT NULL,
            citizen_email TEXT,
            complaint_text TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            department TEXT,
            summary TEXT,
            confidence REAL,
            urgency_reason TEXT,
            location TEXT,
            suggested_action TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            assigned_officer TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Complaint updates table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaint_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            note TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES complaints(id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database tables created successfully!")


def get_db_connection():
    conn = sqlite3.connect("nagrik_ai.db")
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    create_database()