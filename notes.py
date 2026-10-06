#!/usr/bin/env python3
"""Notes app backed by SQLite."""
import sqlite3, sys
from pathlib import Path

DB = Path("notes.db")

def conn():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT)")
    return c

def add(body):
    with conn() as c:
        c.execute("INSERT INTO notes(body) VALUES (?)", (body,))

def list_all():
    with conn() as c:
        for row in c.execute("SELECT id, body FROM notes ORDER BY id"):
            print(f"{row[0]}: {row[1]}")

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "add":
        add(" ".join(sys.argv[2:]))
    else:
        list_all()
