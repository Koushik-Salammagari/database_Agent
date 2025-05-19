import sqlite3

def get_connection():
    return sqlite3.connect("example.db")

def init_db():
    with open("schema.sql", "r") as f:
        conn = get_connection()
        try:
            conn.executescript(f.read())
        except sqlite3.OperationalError as e:
            if "already exists" not in str(e):
                raise e
        finally:
            conn.close()
