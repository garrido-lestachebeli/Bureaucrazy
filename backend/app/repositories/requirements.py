def requirement_type_map(conn) -> dict[str, int]:
    with conn.cursor() as cur:
        cur.execute("SELECT requirement_type_id, code FROM requirement_type")
        rows = cur.fetchall()
    return {row["code"]: row["requirement_type_id"] for row in rows}

def insert_requirement(conn, game_id: int, spec: dict, type_ids: dict[str, int]) -> int:
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO requirement (
                game_id, organization_id, role_id, requirement_type_id,
                minimum_value, asset_type_id, certification_id, history_organization_id,
                detail, parent_requirement_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (game_id,spec["organization_id"],spec["role_id"],type_ids[spec["code"]],spec["minimum_value"],
                spec["asset_type_id"],spec["certification_id"],spec["history_organization_id"],
                spec.get("detail"),spec.get("parent_requirement_id"),
            ),
        )
        new_id = cur.lastrowid
    alternate = spec.get("alternate")
    if alternate and not spec.get("parent_requirement_id"):
        alternate["parent_requirement_id"] = new_id
        alternate["organization_id"] = spec["organization_id"]
        alternate["role_id"] = spec["role_id"]
        insert_requirement(conn, game_id, alternate, type_ids)
    return new_id

def list_requirements(conn, game_id: int) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT r.requirement_id, r.game_id, r.organization_id, r.role_id,
                   r.minimum_value, r.asset_type_id, r.certification_id,
                   r.history_organization_id, r.detail, r.parent_requirement_id,
                   rt.code,
                   o.name AS organization_name,
                   rl.title AS role_title,
                   a.name AS asset_name,
                   c.name AS certification_name,
                   ho.name AS history_organization_name
            FROM requirement r
            JOIN requirement_type rt ON rt.requirement_type_id = r.requirement_type_id
            LEFT JOIN organization o ON o.organization_id = r.organization_id
            LEFT JOIN role rl ON rl.role_id = r.role_id
            LEFT JOIN asset_type a ON a.asset_type_id = r.asset_type_id
            LEFT JOIN certification c ON c.certification_id = r.certification_id
            LEFT JOIN organization ho ON ho.organization_id = r.history_organization_id
            WHERE r.game_id = %s
            ORDER BY r.requirement_id
            """,
            (game_id,),
        )
        return list(cur.fetchall())


def update_minimum(conn, game_id: int, requirement_id: int, minimum_value: int) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE requirement
            SET minimum_value = %s
            WHERE requirement_id = %s AND game_id = %s
            """,
            (minimum_value, requirement_id, game_id),
        )


def delete_requirement(conn, game_id: int, requirement_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM requirement WHERE requirement_id = %s AND game_id = %s",
            (requirement_id, game_id),
        )
