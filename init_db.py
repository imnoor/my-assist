from const import CHAT_HISTORY_DB
import sqlite3

def get_con():
    return sqlite3.connect(CHAT_HISTORY_DB)

def recreate_db():
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS messages')
    cursor.execute('DROP TABLE IF EXISTS sessions')
    cursor.execute('CREATE TABLE IF NOT EXISTS sessions ( name TEXT UNIQUE NOT NULL, model TEXT NOT NULL,  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )')
    cursor.execute('CREATE TABLE IF NOT EXISTS messages ( session_id INT REFERENCES sessions(rowid) ON DELETE CASCADE, role TEXT NOT NULL, content TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    set_default_session(conn)

def create_db():
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS sessions (  name TEXT UNIQUE NOT NULL, model TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP )')
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (  session_id INT REFERENCES sessions(rowid) ON DELETE CASCADE, role TEXT NOT NULL, content TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    set_default_session(conn)

def set_default_session(conn):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO sessions (name, model) VALUES (?, ?);",
        ("Default", "deepseek-r1:latest")
    )
    conn.commit()

def querry_msg():
    cursor = get_con().cursor()
    cursor.execute("SELECT * FROM messages ORDER BY created_at ASC;")
    print(cursor.fetchall())

def query_ssn():
    cursor = get_con().cursor()
    cursor.execute("SELECT * FROM sessions")
    print(cursor.fetchall())

def clear_db():
    con = get_con()
    con.execute("DELETE FROM messages")
    con.commit()

def insert_data():
    conn = get_con()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO sessions (name, model) VALUES (?, ?);",
        ("Default", "deepseek-r1:latest")
    )
    conn.commit()

#recreate_db()

#clear_db()
#create_db()
#query_ssn()
#querry_msg()
