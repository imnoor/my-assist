from const import CHAT_HISTORY_DB
from init_db import create_db
import sqlite3
import os

def get_db_connection():
    return sqlite3.connect(CHAT_HISTORY_DB)

def first_run():
    db_name = CHAT_HISTORY_DB

    # Check if the file exists
    if os.path.exists(db_name):
        return
    else:
        # Create a new SQLite database
        create_db()
        
# Save session details
def save_session(name, model):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO sessions (name, model) VALUES (?, ?) ON CONFLICT (name) DO NOTHING RETURNING rowid;",
            (name, model)
        )
        #conn.commit()
        #print("saving sessions " + name)
        session_id = cur.fetchone()
        return session_id


# Fetch session by name
def get_session(name):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT rowid, model FROM sessions WHERE name = ?;", (name,))
        session = cur.fetchone()
        #print(session)
        return session


# Fetch all session names
def get_all_sessions():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sessions;")
        return [row[0] for row in cur.fetchall()]


# Save message
def save_message(session_id, role, content):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?);",
                    (session_id, role, content))
        conn.commit()


# Fetch chat history from database
def get_chat_history(session_id):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at ASC;", (session_id,))
        return cur.fetchall()
