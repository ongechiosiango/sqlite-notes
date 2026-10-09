"""Data access for notes."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass


class StoreError(Exception):
    """Raised when a store operation fails."""


@dataclass
class Note:
    id: int
    body: str
    created_at: str


def add_note(conn: sqlite3.Connection, body: str) -> Note:
    """Insert a note and return it."""
    body = (body or "").strip()
    if not body:
        raise StoreError("Note body cannot be empty.")

    cur = conn.execute("INSERT INTO notes (body) VALUES (?)", (body,))
    conn.commit()
    return get_note(conn, cur.lastrowid)


def get_note(conn: sqlite3.Connection, note_id: int) -> Note:
    """Fetch one note by ID. Raises StoreError if missing."""
    row = conn.execute(
        "SELECT id, body, created_at FROM notes WHERE id = ?", (note_id,)
    ).fetchone()
    if row is None:
        raise StoreError(f"Note {note_id} not found.")
    return Note(id=row["id"], body=row["body"], created_at=row["created_at"])


def list_notes(conn: sqlite3.Connection) -> list:
    """Return all notes, newest first."""
    rows = conn.execute(
        "SELECT id, body, created_at FROM notes ORDER BY id DESC"
    ).fetchall()
    return [Note(id=r["id"], body=r["body"], created_at=r["created_at"]) for r in rows]
