# Usage Guide

## Add a note

    notes add "Buy milk"

## List notes

    notes list

Notes are shown newest first.

## Where notes are stored

By default, the database lives at:

    ~/.sqlite-notes/notes.db

To use a different location:

    notes --db ./my-notes.db add "hello"

Or set the NOTES_DB environment variable:

    export NOTES_DB=~/work-notes.db
    notes add "hello"

## Exit codes

- 0 - success
- 1 - invalid input (e.g., empty note)
