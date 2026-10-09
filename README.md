# SQLite Notes

[![CI](https://github.com/ongechiosiango/sqlite-notes/actions/workflows/ci.yml/badge.svg)](https://github.com/ongechiosiango/sqlite-notes/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A tiny command-line notes app backed by SQLite.

## Features

- Add and list notes from the terminal.
- Stores data in a single SQLite file.
- Rich terminal output with a clean table.
- No server, no account, no sync. Just your notes.

**Roadmap:** delete, show by id, tags, full-text search (FTS5), JSON/Markdown export.

## Installation

From source:

    git clone git@github.com:ongechiosiango/sqlite-notes.git
    cd sqlite-notes
    python3 -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"

## Usage

    notes add "Buy milk"
    notes list

By default, notes live in `~/.sqlite-notes/notes.db`.
Override with `--db PATH` or the `NOTES_DB` env var.

See docs/usage.md for full details.

## Development

    pip install -e ".[dev]"
    pytest -v

## Contributing

See CONTRIBUTING.md.

## License

MIT - see LICENSE.
