"""Minimal PostgreSQL setup for the CheckStock MVP."""

import os
from pathlib import Path

import psycopg


MIGRATION = Path(__file__).parent / "migrations" / "001_initial_schema.sql"


def initialize_database() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise SystemExit("DATABASE_URL is not set. Copy .env.example to .env and export its values.")

    try:
        with psycopg.connect(database_url) as connection:
            connection.execute(MIGRATION.read_text(encoding="utf-8"))
    except psycopg.Error as error:
        raise SystemExit(f"Could not initialize PostgreSQL schema: {error}") from None

    print("CheckStock PostgreSQL schema is ready.")


if __name__ == "__main__":
    initialize_database()
