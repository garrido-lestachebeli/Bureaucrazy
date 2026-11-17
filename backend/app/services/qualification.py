from datetime import date


def years_experience(employment, today: date) -> float:
    # Overlapping jobs are added separately. A person with two jobs at once
    # counts both stretches toward the experience rule.
    total_days = 0
    for job in employment:
        start = job["start_date"]
        end = job["end_date"] or today
        if start is None or end < start:
            continue
        total_days += (end - start).days
    return total_days / 365


def _years(value: int) -> str:
    unit = "year" if value == 1 else "years"
    return f"{value} {unit}"


def describe_requirement(req: dict) -> str:
    code = req["code"]
    if code == "min_age":
        return f"At least {req['minimum_value']} years old"
    if code == "min_ownership":
        return f"Own at least {req['minimum_value']} ({req['asset_name']})"
    if code == "has_certification":
        return f"Hold a {req['certification_name']} license"
    if code == "prior_agency":
        return f"Have worked for {req['history_organization_name']}"
    if code == "min_experience":
        return f"At least {_years(req['minimum_value'])} of work experience"
    raise ValueError(f"Unknown requirement type: {code}")


def evaluate_requirement(req: dict, person: dict, today: date) -> tuple[bool, str]:
    label = describe_requirement(req)
    code = req["code"]
    if code == "min_age":
        return person["age"] >= req["minimum_value"], label
    if code == "min_ownership":
        owned = person["assets"].get(req["asset_type_id"], 0)
        return owned >= req["minimum_value"], label
    if code == "has_certification":
        return req["certification_id"] in person["certification_ids"], label
    if code == "prior_agency":
        worked = any(
            job["organization_id"] == req["history_organization_id"] for job in person["employment"]
        )
        return worked, label
    if code == "min_experience":
        return years_experience(person["employment"], today) >= req["minimum_value"], label
    raise ValueError(f"Unknown requirement type: {code}")


def evaluate_all(requirements, person: dict, today: date | None = None) -> tuple[bool, list[str]]:
    today = today or date.today()
    failed = []
    for req in requirements:
        ok, label = evaluate_requirement(req, person, today)
        if not ok:
            failed.append(label)
    return len(failed) == 0, failed
