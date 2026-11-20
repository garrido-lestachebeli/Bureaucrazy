from datetime import date

import pymysql
import pytest
from fastapi.testclient import TestClient

from app.db import connection
from app.repositories.requirements import list_requirements
from app.repositories.world import fetch_catalog, fetch_people
from app.services.qualification import evaluate_all


@pytest.fixture
def client(database):
    from app.main import app

    return TestClient(app)


def test_known_applicants_and_referential_checks(database):
    with connection() as conn:
        people = {person["full_name"]: person for person in fetch_people(conn)}
        catalog = fetch_catalog(conn)
        marisol = people["Marisol Vega"]
        lena = people["Lena Cho"]
        felix = people["Felix Navarro"]
        assert marisol["age"] == 52
        assert len(marisol["employment"]) == 2
        assert felix["age"] == 19
        assert felix["employment"] == []
        assert felix["certification_ids"] == set()

        notary = next(item for item in catalog["certifications"] if item["name"] == "Notary")
        requirements = [
            {"code": "min_age", "minimum_value": 25},
            {
                "code": "has_certification",
                "certification_id": notary["certification_id"],
                "certification_name": "Notary",
            },
            {"code": "min_experience", "minimum_value": 10},
        ]
        qualified, failed = evaluate_all(requirements, lena, today=date(2026, 11, 5))
        assert qualified is False
        assert len(failed) == 1
        assert "10 years" in failed[0]

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


def _force_impossible_age(game_id):
    with connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM requirement WHERE game_id = %s", (game_id,))
            cur.execute("SELECT requirement_type_id FROM requirement_type WHERE code = 'min_age'")
            type_id = cur.fetchone()["requirement_type_id"]
            cur.execute("SELECT organization_id FROM organization ORDER BY organization_id LIMIT 1")
            org_id = cur.fetchone()["organization_id"]
            cur.execute(
                """
                INSERT INTO requirement (
                    game_id, organization_id, role_id, requirement_type_id, minimum_value
                ) VALUES (%s, %s, NULL, %s, 200)
                """,
                (game_id, org_id, type_id),
            )


def test_case_hides_the_answer_and_bad_approvals_lose_the_day(client):
    created = client.post("/api/games")
    assert created.status_code == 201
    game_id = created.json()["game_id"]
    _force_impossible_age(game_id)

    payload = None
    for _ in range(5):
        case = client.get(f"/api/games/{game_id}/case")
        assert case.status_code == 200
        body = case.json()
        assert body["sentence"].startswith("I want to work for The ")
        assert " as a " in body["sentence"] or " as an " in body["sentence"]
        assert "selection_band" not in body
        assert "actual_outcome" not in body
        folder = body["rule_folder"]
        assert len(folder["organizations"]) == 8
        assert len(folder["roles"]) == 8
        org_names = [sheet["name"] for sheet in folder["organizations"]]
        assert org_names == sorted(org_names)
        assert all("applies" not in sheet for sheet in folder["organizations"] + folder["roles"])
        decision = client.post(
            f"/api/games/{game_id}/decision",
            json={"decision": "approve"},
        )
        assert decision.status_code == 200
        payload = decision.json()
        assert payload["correct"] is False
        assert payload["actual_outcome"] == "not_qualified"

    assert payload["day_complete"] is True
    assert payload["mistakes_on_day"] == 5
    assert payload["game"]["status"] == "lost"
    assert payload["game"]["current_day"] == 1


def test_a_clean_day_advances_and_keeps_the_old_outcome(client):
    created = client.post("/api/games")
    game_id = created.json()["game_id"]
    _force_impossible_age(game_id)

    payload = None
    for _ in range(5):
        case = client.get(f"/api/games/{game_id}/case")
        assert case.status_code == 200
        decision = client.post(f"/api/games/{game_id}/decision", json={"decision": "deny"})
        payload = decision.json()
        assert payload["correct"] is True

    assert payload["advanced"] is True
    assert payload["game"]["status"] == "active"
    assert payload["game"]["current_day"] == 2
    assert client.get(f"/api/games/{game_id}/case").status_code == 200

    history = client.get(f"/api/games/{game_id}/history")
    day_one = [row for row in history.json()["requests"] if row["day_number"] == 1]
    assert len(day_one) == 5
    assert all(row["decision_correct"] for row in day_one)
    assert all("200" in (row["outcome_detail"] or "") for row in day_one)


def test_correct_days_keep_the_desk_open(client):
    created = client.post("/api/games")
    game_id = created.json()["game_id"]
    payload = None
    for _ in range(25):
        case = client.get(f"/api/games/{game_id}/case")
        assert case.status_code == 200
        body = case.json()
        with connection() as conn:
            people = {person["person_id"]: person for person in fetch_people(conn)}
            requirements = list_requirements(conn, game_id)
        person = people[body["applicant"]["person_id"]]
        applicable = [
            req
            for req in requirements
            if req["organization_id"] == body["organization"]["organization_id"]
            or req["role_id"] == body["role"]["role_id"]
        ]
        qualified, _failed = evaluate_all(applicable, person)
        choice = "approve" if qualified else "deny"
        decision = client.post(f"/api/games/{game_id}/decision", json={"decision": choice})
        assert decision.status_code == 200
        payload = decision.json()
        assert payload["correct"] is True

    assert payload["game"]["status"] == "active"
    assert payload["day_number"] == 5
    assert payload["game"]["current_day"] == 6
