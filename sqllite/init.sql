-- Create sessions table
CREATE TABLE IF NOT EXISTS sessions (
    name TEXT UNIQUE NOT NULL,
    model TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    session_id INT REFERENCES sessions(ROWID) ON DELETE CASCADE,
    role TEXT NOT NULL, -- "user" or "assistant"
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
