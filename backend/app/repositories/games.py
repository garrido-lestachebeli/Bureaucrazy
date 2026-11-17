def insert_game(conn) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO game (
                current_day, status, weight_qualified, weight_nearly,
                weight_not_close, mistakes_allowed
            ) VALUES (1, 'active', 60, 30, 10, 1)
            """
        )
        return cur.lastrowid


def lock_game(conn, game_id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM game WHERE game_id = %s FOR UPDATE", (game_id,))
        return cur.fetchone()


def update_game_progress(conn, game_id: int, current_day: int, status: str) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE game SET current_day = %s, status = %s WHERE game_id = %s",
            (current_day, status, game_id),
        )
