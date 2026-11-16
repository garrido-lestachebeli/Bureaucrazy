import pymysql
import pytest

from app.db import connection
from app.repositories.world import fetch_catalog, fetch_people


def test_known_applicants_and_referential_checks(database):
    with connection() as conn:
        people = {person["full_name"]: person for person in fetch_people(conn)}
        catalog = fetch_catalog(conn)
        marisol = people["Marisol Vega"]
        felix = people["Felix Navarro"]
        assert marisol["age"] == 52
        assert len(marisol["employment"]) == 2
        assert felix["age"] == 19
        assert felix["employment"] == []
        assert felix["certification_ids"] == set()
        assert len(catalog["organizations"]) == 8
        assert len(catalog["roles"]) == 8

        with conn.cursor() as cur:
            with pytest.raises(pymysql.err.OperationalError):
                cur.execute("INSERT INTO person (full_name, age) VALUES ('Too Young', -1)")
            cur.execute(
                """
                INSERT INTO game (
                    current_day, status, weight_qualified, weight_nearly,
                    weight_not_close, mistakes_allowed
                ) VALUES (1, 'active', 60, 30, 10, 1)
                """
            )
            game_id = cur.lastrowid
            cur.execute("SELECT requirement_type_id FROM requirement_type WHERE code = 'min_age'")
            type_id = cur.fetchone()["requirement_type_id"]
            cur.execute("SELECT organization_id FROM organization ORDER BY organization_id LIMIT 1")
            org_id = cur.fetchone()["organization_id"]
            cur.execute("SELECT role_id FROM role ORDER BY role_id LIMIT 1")
            role_id = cur.fetchone()["role_id"]
            with pytest.raises(pymysql.err.OperationalError):
                cur.execute(
                    """
                    INSERT INTO requirement (
                        game_id, organization_id, role_id, requirement_type_id, minimum_value
                    ) VALUES (%s, %s, %s, %s, 21)
                    """,
                    (game_id, org_id, role_id, type_id),
                )
