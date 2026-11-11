from contextlib import contextmanager

import pymysql
from pymysql.cursors import DictCursor

from app.config import Settings, get_settings


def server_connection(settings: Settings | None = None, database: str | None = None):
    settings = settings or get_settings()
    return pymysql.connect(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=database,
        charset="utf8mb4",
        collation="utf8mb4_0900_ai_ci",
        cursorclass=DictCursor,
        autocommit=False,
    )


@contextmanager
def connection():
    conn = server_connection(database=get_settings().mysql_database)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
