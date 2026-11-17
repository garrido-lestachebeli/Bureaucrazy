from app.services.qualification import evaluate_all


def draw_case(people: list[dict], pairs: list[tuple], rng, today=None) -> dict:
    """Pick a posting, then an applicant. About half the draws are qualified."""
    if not people:
        raise ValueError("No applicants")
    if not pairs:
        raise ValueError("No postings")
    organization_id, role_id, requirements = rng.choice(pairs)
    qualified = []
    unqualified = []
    for person in people:
        passed, _failed = evaluate_all(requirements, person, today=today)
        (qualified if passed else unqualified).append(person)
    want_qualified = rng.random() < 0.5
    pool = qualified if (want_qualified and qualified) or not unqualified else unqualified
    chosen = rng.choice(pool)
    return {
        "organization_id": organization_id,
        "role_id": role_id,
        "person": chosen,
        "selection_band": "qualified" if pool is qualified else "not_close",
    }


def posting_pairs(requirements: list[dict], catalog: dict) -> list[tuple]:
    org_ids = []
    role_ids = []
    seen_orgs = set()
    seen_roles = set()
    for req in requirements:
        if req["organization_id"] and req["organization_id"] not in seen_orgs:
            seen_orgs.add(req["organization_id"])
            org_ids.append(req["organization_id"])
        if req["role_id"] and req["role_id"] not in seen_roles:
            seen_roles.add(req["role_id"])
            role_ids.append(req["role_id"])
    if not org_ids:
        org_ids = [org["organization_id"] for org in catalog["organizations"]]
    if not role_ids:
        role_ids = [role["role_id"] for role in catalog["roles"]]
    pairs = []
    for organization_id in org_ids:
        for role_id in role_ids:
            applicable = [
                req
                for req in requirements
                if req["organization_id"] == organization_id or req["role_id"] == role_id
            ]
            if applicable:
                pairs.append((organization_id, role_id, applicable))
    return pairs
