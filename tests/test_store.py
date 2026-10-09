"""Tests for the notes store."""

import pytest

from sqlite_notes.db import migrate, open_db
from sqlite_notes.store import StoreError, add_note, delete_note, get_note, list_notes


@pytest.fixture
def conn():
    c = open_db(":memory:")
    migrate(c)
    yield c
    c.close()


def test_add_note_returns_note(conn):
    note = add_note(conn, "Buy milk")
    assert note.id == 1
    assert note.body == "Buy milk"
    assert note.created_at


def test_add_note_strips_whitespace(conn):
    note = add_note(conn, "   hello   ")
    assert note.body == "hello"


def test_add_note_rejects_empty(conn):
    with pytest.raises(StoreError, match="empty"):
        add_note(conn, "")
    with pytest.raises(StoreError, match="empty"):
        add_note(conn, "   ")


def test_list_notes_newest_first(conn):
    add_note(conn, "first")
    add_note(conn, "second")
    add_note(conn, "third")
    notes = list_notes(conn)
    assert [n.body for n in notes] == ["third", "second", "first"]


def test_list_notes_empty(conn):
    assert list_notes(conn) == []


def test_get_note_missing_raises(conn):
    with pytest.raises(StoreError, match="not found"):
        get_note(conn, 999)


def test_delete_note_removes_it(conn):
    note = add_note(conn, "to delete")
    delete_note(conn, note.id)
    with pytest.raises(StoreError, match="not found"):
        get_note(conn, note.id)


def test_delete_missing_raises(conn):
    with pytest.raises(StoreError, match="not found"):
        delete_note(conn, 999)
