import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import pymysql

from app.config import get_settings
from app.database_setup import reset_database


def main() -> None:
    settings = get_settings()
    try:
        reset_database(settings.mysql_database, settings)
    except pymysql.MySQLError as exc:
        message = exc.args[1] if len(exc.args) > 1 else str(exc)
        raise SystemExit(f"Could not set up MySQL: {message}") from exc
    print(f"Loaded {settings.mysql_database}.")


if __name__ == "__main__":
    main()
