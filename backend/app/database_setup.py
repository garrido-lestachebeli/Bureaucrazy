import re

import pymysql

from app.config import ROOT, Settings, get_settings
from app.db import server_connection

SAFE_NAME = re.compile(r"^bureaucrazy[A-Za-z0-9_]*$")


def assert_safe_name(name: str) -> None:
    if not SAFE_NAME.fullmatch(name):
        raise ValueError(
            f"Refusing to reset {name!r}. The database name must start with 'bureaucrazy'."
        )


def split_sql(script: str) -> list[str]:
    statements = []
    buffer: list[str] = []
    for line in script.splitlines():
        stripped = line.strip()
        if stripped.startswith("--"):
            continue
        buffer.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(buffer).strip()
            if statement.endswith(";"):
                statement = statement[:-1].strip()
            if statement:
                statements.append(statement)
            buffer = []
    leftover = "\n".join(buffer).strip()
    if leftover:
        statements.append(leftover)
    return statements


def apply_script(conn, path) -> None:
    script = path.read_text(encoding="utf-8")
    with conn.cursor() as cur:
        for statement in split_sql(script):
            cur.execute(statement)


def can_connect(settings: Settings | None = None) -> bool:
    try:
        conn = server_connection(settings, database=None)
    except pymysql.MySQLError:
        return False
    conn.close()
    return True


def reset_database(name: str, settings: Settings | None = None) -> None:
    assert_safe_name(name)
    settings = settings or get_settings()
    admin = server_connection(settings, database=None)
    try:
        with admin.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS `{name}`")
            cur.execute(
                f"CREATE DATABASE `{name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
            )
        admin.commit()
    finally:
        admin.close()

    conn = server_connection(settings, database=name)
    try:
        apply_script(conn, ROOT / "database" / "schema.sql")
        apply_script(conn, ROOT / "database" / "seed_world.sql")
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
