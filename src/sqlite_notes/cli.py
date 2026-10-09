"""Command-line interface for SQLite Notes."""

from __future__ import annotations

import argparse

from rich.console import Console

from . import __version__
from .db import default_db_path, migrate, open_db
from .reporter import print_deleted, print_note, print_notes, print_single_note
from .store import StoreError, add_note, delete_note, get_note, list_notes

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="notes",
        description="A tiny command-line notes app backed by SQLite.",
    )
    parser.add_argument("--version", action="version", version=f"sqlite-notes {__version__}")
    parser.add_argument(
        "--db", default=None,
        help=f"Path to the SQLite database (default: {default_db_path()})",
    )

    sub = parser.add_subparsers(dest="cmd", required=True)

    add_p = sub.add_parser("add", help="Add a new note.")
    add_p.add_argument("body", help="The note text.")

    sub.add_parser("list", help="List all notes, newest first.")

    show_p = sub.add_parser("show", help="Show a single note by ID.")
    show_p.add_argument("id", type=int, help="Note ID.")

    delete_p = sub.add_parser("delete", help="Delete a note by ID.")
    delete_p.add_argument("id", type=int, help="Note ID.")

    return parser


def main() -> int:
    args = build_parser().parse_args()

    conn = open_db(args.db)
    migrate(conn)

    try:
        if args.cmd == "add":
            try:
                note = add_note(conn, args.body)
            except StoreError as exc:
                console.print(f"[bold red]Error:[/bold red] {exc}")
                return 1
            print_note(note, action="Saved")
            return 0

        if args.cmd == "list":
            print_notes(list_notes(conn))
            return 0

        if args.cmd == "show":
            try:
                note = get_note(conn, args.id)
            except StoreError as exc:
                console.print(f"[bold red]Error:[/bold red] {exc}")
                return 1
            print_single_note(note)
            return 0

        if args.cmd == "delete":
            try:
                delete_note(conn, args.id)
            except StoreError as exc:
                console.print(f"[bold red]Error:[/bold red] {exc}")
                return 1
            print_deleted(args.id)
            return 0
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
