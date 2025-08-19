import sqlite3
from contextlib import contextmanager

DB_NAME = "permissions.db"

@contextmanager
def db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()

def init_tables():
    with db() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS user_permissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            action TEXT NOT NULL,    -- 'read','write','delete' or '*'
            resource TEXT NOT NULL,  -- 'transactions', 'wallets/*', etc.
            effect TEXT NOT NULL     -- 'allow' or 'deny'
        )
        """)
        conn.commit()
