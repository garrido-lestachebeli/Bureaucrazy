from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.db import connection
from app.errors import GameError
from app.services.gameplay import game_state, get_case, history, start_game, submit_decision

router = APIRouter()


class DecisionBody(BaseModel):
    decision: Literal["approve", "deny"]


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


@router.post("/games", status_code=201)
def create_game():
    return _call(start_game)


@router.get("/games/{game_id}")
def read_game(game_id: int):
    return _call(lambda conn: game_state(conn, game_id))


@router.get("/games/{game_id}/case")
def read_case(game_id: int):
    return _call(lambda conn: get_case(conn, game_id))


@router.post("/games/{game_id}/decision")
def decide(game_id: int, body: DecisionBody):
    return _call(lambda conn: submit_decision(conn, game_id, body.decision))


@router.get("/games/{game_id}/history")
def read_history(game_id: int):
    return _call(lambda conn: history(conn, game_id))
