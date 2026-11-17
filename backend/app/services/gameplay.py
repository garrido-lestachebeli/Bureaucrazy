import random

from app.constants import CASES_PER_DAY
from app.errors import GameError
from app.repositories.games import insert_game, lock_game
from app.repositories.requests import (
    count_judged,
    count_mistakes,
    delete_open_case,
    insert_open_case,
    insert_reviewed_request,
    lock_open_case,
)
from app.repositories.requirements import (
    insert_requirement,
    list_requirements,
    requirement_type_map,
)
from app.repositories.world import fetch_catalog, fetch_people
from app.services.applicants import draw_case, posting_pairs
from app.services.generation import ALL_CODES, build_starting_requirements
from app.services.qualification import describe_requirement, evaluate_all


def request_sentence(organization_name: str, role_title: str) -> str:
    agency = organization_name
    if not agency.lower().startswith("the "):
        agency = f"The {agency}"
    article = "an" if role_title[:1].lower() in "aeiou" else "a"
    return f"I want to work for {agency} as {article} {role_title}."


def _require_world(catalog: dict, people: list[dict]) -> None:
    if (
        not catalog["organizations"]
        or not catalog["roles"]
        or not catalog["certifications"]
        or not catalog["assets"]
        or not people
    ):
        raise GameError(500, "World data is not loaded.")


def applicant_file(person: dict, catalog: dict) -> dict:
    cert_names = sorted(
        cert["name"]
        for cert in catalog["certifications"]
        if cert["certification_id"] in person["certification_ids"]
    )
    asset_names = {asset["asset_type_id"]: asset["name"] for asset in catalog["assets"]}
    assets = [
        {"name": asset_names[asset_id], "quantity": quantity}
        for asset_id, quantity in person["assets"].items()
        if quantity > 0 and asset_id in asset_names
    ]
    assets.sort(key=lambda item: item["name"])
    jobs = []
    for job in person["employment"]:
        start = job["start_date"].strftime("%b %Y")
        end = "present" if job["end_date"] is None else job["end_date"].strftime("%b %Y")
        jobs.append(
            {
                "organization": job["organization_name"],
                "title": job["role_title"],
                "span": f"{start} – {end}",
            }
        )
    return {
        "person_id": person["person_id"],
        "full_name": person["full_name"],
        "age": person["age"],
        "file_number": f"P-{person['person_id']:04d}",
        "certifications": cert_names,
        "assets": assets,
        "jobs": jobs,
    }


def game_state(conn, game_id: int) -> dict:
    game = lock_game(conn, game_id)
    if not game:
        raise GameError(404, "No such game.")
    judged = count_judged(conn, game_id, game["current_day"])
    mistakes = count_mistakes(conn, game_id, game["current_day"])
    return {
        "game_id": game["game_id"],
        "current_day": game["current_day"],
        "status": game["status"],
        "mistakes_allowed": game["mistakes_allowed"],
        "cases_per_day": CASES_PER_DAY,
        "cases_judged_today": judged,
        "cases_left": max(0, CASES_PER_DAY - judged),
        "mistakes_today": mistakes,
    }


def rule_folder(requirements: list[dict], catalog: dict) -> dict:
    org_rules: dict[str, list[str]] = {}
    role_rules: dict[str, list[str]] = {}
    for req in requirements:
        text = describe_requirement(req)
        if req["organization_id"]:
            org_rules.setdefault(req["organization_name"], []).append(text)
        else:
            role_rules.setdefault(req["role_title"], []).append(text)

    def sheets(rows, name_field, grouped):
        pages = []
        for row in rows:
            pages.append(
                {
                    "name": row[name_field],
                    "rules": sorted(grouped.get(row[name_field], [])),
                }
            )
        pages.sort(key=lambda page: page["name"])
        return pages

    return {
        "organizations": sheets(catalog["organizations"], "name", org_rules),
        "roles": sheets(catalog["roles"], "title", role_rules),
    }


def _case_payload(conn, organization_id, role_id, person, organization_name, role_title, requirements):
    catalog = fetch_catalog(conn)
    return {
        "sentence": request_sentence(organization_name, role_title),
        "organization": {"organization_id": organization_id, "name": organization_name},
        "role": {"role_id": role_id, "title": role_title},
        "rule_folder": rule_folder(requirements, catalog),
        "applicant": applicant_file(person, catalog),
    }


def start_game(conn, rng=None) -> dict:
    rng = rng or random.Random()
    catalog = fetch_catalog(conn)
    people = fetch_people(conn)
    _require_world(catalog, people)
    type_ids = requirement_type_map(conn)
    if any(code not in type_ids for code in ALL_CODES):
        raise GameError(500, "Requirement types are not loaded.")
    game_id = insert_game(conn)
    for spec in build_starting_requirements(catalog, rng):
        insert_requirement(conn, game_id, spec, type_ids)
    return game_state(conn, game_id)


def get_case(conn, game_id: int, rng=None) -> dict:
    rng = rng or random.Random()
    game = lock_game(conn, game_id)
    if not game:
        raise GameError(404, "No such game.")
    if game["status"] != "active":
        raise GameError(409, "This game is already over.")
    if count_judged(conn, game_id, game["current_day"]) >= CASES_PER_DAY:
        raise GameError(409, "This day is already closed.")

    existing = lock_open_case(conn, game_id)
    requirements = list_requirements(conn, game_id)
    people = fetch_people(conn)
    if not existing:
        catalog = fetch_catalog(conn)
        pairs = posting_pairs(requirements, catalog)
        if not pairs:
            raise GameError(500, "This game has no rules to post.")
        drawn = draw_case(people, pairs, rng)
        insert_open_case(conn, game_id, drawn)
        existing = lock_open_case(conn, game_id)

    person = next(item for item in people if item["person_id"] == existing["person_id"])
    return _case_payload(
        conn,
        existing["organization_id"],
        existing["role_id"],
        person,
        existing["organization_name"],
        existing["role_title"],
        requirements,
    )


def submit_decision(conn, game_id: int, decision: str) -> dict:
    if decision not in {"approve", "deny"}:
        raise GameError(422, "Decision must be approve or deny.")
    game = lock_game(conn, game_id)
    if not game:
        raise GameError(404, "No such game.")
    if game["status"] != "active":
        raise GameError(409, "This game is already over.")
    case = lock_open_case(conn, game_id)
    if not case:
        raise GameError(409, "There is no request on the desk.")

    people = fetch_people(conn)
    person = next(item for item in people if item["person_id"] == case["person_id"])
    requirements = list_requirements(conn, game_id)
    applicable = [
        req
        for req in requirements
        if req["organization_id"] == case["organization_id"] or req["role_id"] == case["role_id"]
    ]
    qualified, failed = evaluate_all(applicable, person)
    actual = "qualified" if qualified else "not_qualified"
    correct = (decision == "approve" and qualified) or (decision == "deny" and not qualified)
    detail = "; ".join(failed) if failed else None
    if detail and len(detail) > 500:
        detail = detail[:497] + "..."

    judged_day = game["current_day"]
    insert_reviewed_request(
        conn,
        {
            "game_id": game_id,
            "day_number": judged_day,
            "organization_id": case["organization_id"],
            "role_id": case["role_id"],
            "person_id": case["person_id"],
            "selection_band": case["selection_band"],
            "player_decision": decision,
            "actual_outcome": actual,
            "decision_correct": correct,
            "outcome_detail": detail,
        },
    )
    delete_open_case(conn, game_id)

    mistakes_on_day = count_mistakes(conn, game_id, judged_day)
    day_complete = count_judged(conn, game_id, judged_day) >= CASES_PER_DAY

    return {
        "correct": correct,
        "actual_outcome": actual,
        "player_decision": decision,
        "sentence": request_sentence(case["organization_name"], case["role_title"]),
        "applicant_name": person["full_name"],
        "failed_requirements": failed,
        "day_number": judged_day,
        "day_complete": day_complete,
        "mistakes_on_day": mistakes_on_day,
        "game": game_state(conn, game_id),
    }
