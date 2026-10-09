"""Tests for the CLI."""

import pytest

from sqlite_notes.cli import build_parser
from sqlite_notes.db import migrate, open_db
from sqlite_notes.store import add_note, list_notes


@pytest.fixture
def conn():
    c = open_db(":memory:")
    migrate(c)
    yield c
    c.close()


def test_parser_requires_subcommand():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_parser_add_accepts_body():
    parser = build_parser()
    args = parser.parse_args(["add", "hello world"])
    assert args.cmd == "add"
    assert args.body == "hello world"


def test_parser_list():
    parser = build_parser()
    args = parser.parse_args(["list"])
    assert args.cmd == "list"


def test_end_to_end_add_then_list(conn):
    add_note(conn, "from cli")
    notes = list_notes(conn)
    assert len(notes) == 1
    assert notes[0].body == "from cli"


def test_parser_show_requires_id():
    parser = build_parser()
    args = parser.parse_args(["show", "3"])
    assert args.cmd == "show"
    assert args.id == 3


def test_parser_delete_requires_id():
    parser = build_parser()
    args = parser.parse_args(["delete", "7"])
    assert args.cmd == "delete"
    assert args.id == 7
