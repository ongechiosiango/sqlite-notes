"""Rich terminal output."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def print_note(note, action: str = "Saved") -> None:
    console.print(f"[green]{action}[/green] note [bold]#{note.id}[/bold]: {note.body}")


def print_deleted(note_id: int) -> None:
    console.print(f"[green]Deleted[/green] note [bold]#{note_id}[/bold].")


def print_single_note(note) -> None:
    body = f"[bold cyan]#{note.id}[/bold cyan]  [dim]{note.created_at}[/dim]\n\n{note.body}"
    console.print(Panel(body, title="Note", border_style="cyan"))


def print_notes(notes) -> None:
    if not notes:
        console.print('[yellow]No notes yet.[/yellow] Add one with: notes add "..."')
        return

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", justify="right", no_wrap=True)
    table.add_column("Created", style="dim", no_wrap=True)
    table.add_column("Note", style="white")

    for n in notes:
        table.add_row(str(n.id), n.created_at, n.body)

    console.print(table)
