AGE_OPTIONS = (18, 21, 25, 30, 35, 40)
OWNERSHIP_OPTIONS = (1, 2, 3)
EXPERIENCE_OPTIONS = (1, 2, 3, 4, 5)
SIMPLE_CODES = (
    "min_age",
    "min_ownership",
    "has_certification",
    "prior_agency",
    "min_experience",
)
CODES = SIMPLE_CODES
ALL_CODES = CODES


def blank_spec(code: str, organization_id, role_id) -> dict:
    return {
        "code": code,
        "organization_id": organization_id,
        "role_id": role_id,
        "minimum_value": None,
        "asset_type_id": None,
        "certification_id": None,
        "history_organization_id": None,
        "detail": None,
    }


def rule_key(spec: dict) -> tuple:
    return (
        spec["code"],
        spec.get("organization_id"),
        spec.get("role_id"),
        spec.get("asset_type_id"),
        spec.get("certification_id"),
        spec.get("history_organization_id"),
    )


def fill_spec(spec: dict, catalog: dict, rng) -> dict:
    code = spec["code"]
    if code == "min_age":
        spec["minimum_value"] = rng.choice(AGE_OPTIONS)
    elif code == "min_ownership":
        spec["minimum_value"] = rng.choice(OWNERSHIP_OPTIONS)
        spec["asset_type_id"] = rng.choice(catalog["assets"])["asset_type_id"]
    elif code == "has_certification":
        spec["certification_id"] = rng.choice(catalog["certifications"])["certification_id"]
    elif code == "prior_agency":
        spec["history_organization_id"] = rng.choice(catalog["organizations"])["organization_id"]
    elif code == "min_experience":
        spec["minimum_value"] = rng.choice(EXPERIENCE_OPTIONS)
    else:
        raise ValueError(f"Unknown requirement type: {code}")
    return spec


def make_rule(
    owner_kind: str,
    owner_id: int,
    catalog: dict,
    rng,
    existing_keys: set,
    codes=CODES,
) -> dict | None:
    for _ in range(40):
        code = rng.choice(codes)
        organization_id = owner_id if owner_kind == "organization" else None
        role_id = owner_id if owner_kind == "role" else None
        spec = fill_spec(blank_spec(code, organization_id, role_id), catalog, rng)
        key = rule_key(spec)
        if key not in existing_keys:
            existing_keys.add(key)
            return spec
    return None


def _one_rule_each(owners: list[dict], owner_kind: str, id_field: str, catalog: dict, rng, keys: set):
    specs = []
    for owner in owners:
        spec = make_rule(owner_kind, owner[id_field], catalog, rng, keys)
        if not spec:
            raise ValueError(f"Could not give {owner_kind} {owner[id_field]} a requirement")
        specs.append(spec)
    return specs


def build_starting_requirements(catalog: dict, rng) -> list[dict]:
    orgs = list(catalog["organizations"])
    roles = list(catalog["roles"])
    if not orgs or not roles:
        raise ValueError("Organizations and roles are required")
    keys: set = set()
    specs = _one_rule_each(orgs, "organization", "organization_id", catalog, rng, keys)
    specs += _one_rule_each(roles, "role", "role_id", catalog, rng, keys)
    return specs
