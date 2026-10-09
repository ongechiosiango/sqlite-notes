"""Open the SQLite database and apply schema migrations."""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path


def default_db_path() -> Path:
    """Default DB path: ~/.sqlite-notes/notes.db, overridable via NOTES_DB env var."""
    env = os.environ.get("NOTES_DB")
    if env:
        return Path(env)
    return Path.home() / ".sqlite-notes" / "notes.db"


def open_db(path=None) -> sqlite3.Connection:
    """Open a SQLite connection. Use ':memory:' for tests."""
    target = path if path else default_db_path()

    if str(target) != ":memory:":
        Path(target).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(str(target))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist. Safe to call every run."""
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS notes (
          id         INTEGER PRIMARY KEY AUTOINCREMENT,
          body       TEXT NOT NULL,
          created_at TEXT NOT NULL DEFAULT (datetime('now'))
        );
        """
    )
    conn.commit()
