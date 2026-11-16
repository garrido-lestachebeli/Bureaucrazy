from fastapi import APIRouter, HTTPException

from app.db import connection
from app.errors import GameError

router = APIRouter()


def _call(work):
    try:
        with connection() as conn:
            return work(conn)
    except GameError as exc:
        raise HTTPException(status_code=exc.status, detail=exc.message) from exc


@router.get("/health")
def health():
    def check(conn):
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            return cur.fetchone()["ok"] == 1

    return {"status": "ok" if _call(check) else "down"}
