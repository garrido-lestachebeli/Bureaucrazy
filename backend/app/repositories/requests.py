def lock_open_case(conn, game_id: int):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT oc.game_id, oc.organization_id, oc.role_id, oc.person_id, oc.selection_band,
                   oc.drawn_at, o.name AS organization_name, r.title AS role_title
            FROM open_case oc
            JOIN organization o ON o.organization_id = oc.organization_id
            JOIN role r ON r.role_id = oc.role_id
            WHERE oc.game_id = %s
            FOR UPDATE
            """,
            (game_id,),
        )
        return cur.fetchone()


def insert_open_case(conn, game_id: int, draw: dict) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO open_case (
                game_id, organization_id, role_id, person_id, selection_band
            ) VALUES (%s, %s, %s, %s, %s)
            """,
            (game_id,draw["organization_id"],draw["role_id"],draw["person"]["person_id"],
                draw["selection_band"],
            ),
        )


def delete_open_case(conn, game_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM open_case WHERE game_id = %s", (game_id,))


def insert_reviewed_request(conn, row: dict) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO reviewed_request (
                game_id, day_number, organization_id, role_id, person_id,
                selection_band, player_decision, actual_outcome, decision_correct,
                outcome_detail
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                row["game_id"],row["day_number"],row["organization_id"],row["role_id"],
                row["person_id"],row["selection_band"],row["player_decision"],
                row["actual_outcome"],1 if row["decision_correct"] else 0,
                row["outcome_detail"],
            ),
        )
        return cur.lastrowid


def count_judged(conn, game_id: int, day_number: int) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*) AS n
            FROM reviewed_request
            WHERE game_id = %s AND day_number = %s
            """,
            (game_id, day_number),
        )
        return cur.fetchone()["n"]


def count_mistakes(conn, game_id: int, day_number: int) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*) AS n
            FROM reviewed_request
            WHERE game_id = %s AND day_number = %s AND decision_correct = 0
            """,
            (game_id, day_number),
        )
        return cur.fetchone()["n"]


def list_history(conn, game_id: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT rr.request_id, rr.day_number, rr.player_decision, rr.actual_outcome,
                   rr.decision_correct, rr.outcome_detail, rr.reviewed_at,
                   o.name AS organization_name, r.title AS role_title, p.full_name
            FROM reviewed_request rr
            JOIN organization o ON o.organization_id = rr.organization_id
            JOIN role r ON r.role_id = rr.role_id
            JOIN person p ON p.person_id = rr.person_id
            WHERE rr.game_id = %s
            ORDER BY rr.request_id
            """,
            (game_id,),
        )
        rows = list(cur.fetchall())
    history = []
    for row in rows:
        reviewed = row["reviewed_at"]
        history.append(
            {
                "request_id": row["request_id"],
                "day_number": row["day_number"],
                "organization_name": row["organization_name"],
                "role_title": row["role_title"],
                "full_name": row["full_name"],
                "player_decision": row["player_decision"],
                "actual_outcome": row["actual_outcome"],
                "decision_correct": bool(row["decision_correct"]),
                "outcome_detail": row["outcome_detail"],
                "reviewed_at": reviewed.isoformat(sep=" ") if reviewed else None,
            }
        )
    return history
