import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "database.db")

conn = sqlite3.connect(DATABASE)

with open(os.path.join(BASE_DIR, "schema.sql")) as f:
    conn.executescript(f.read())

conn.close()

print("Database initialized successfully.")