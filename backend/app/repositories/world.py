from datetime import date, datetime

def as_date(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    return value

def fetch_catalog(conn) -> dict:
    with conn.cursor() as cur:
        cur.execute("SELECT organization_id, name FROM organization ORDER BY organization_id")
        organizations = list(cur.fetchall())
        cur.execute("SELECT role_id, title FROM role ORDER BY role_id")
        roles = list(cur.fetchall())
        cur.execute("SELECT certification_id, name FROM certification ORDER BY certification_id")
        certifications = list(cur.fetchall())
        cur.execute("SELECT asset_type_id, name FROM asset_type ORDER BY asset_type_id")
        assets = list(cur.fetchall())
        cur.execute("SELECT full_name FROM person ORDER BY person_id")
        people = list(cur.fetchall())
    return {
        "organizations": organizations,
        "roles": roles,
        "certifications": certifications,
        "assets": assets,
        "people": people,
    }

def fetch_people(conn) -> list[dict]:
    with conn.cursor() as cur:
        cur.execute("SELECT person_id, full_name, age FROM person ORDER BY person_id")
        people = list(cur.fetchall())
        cur.execute("SELECT person_id, certification_id FROM person_certification")
        cert_rows = list(cur.fetchall())
        cur.execute("SELECT person_id, asset_type_id, quantity FROM person_asset")
        asset_rows = list(cur.fetchall())
        cur.execute(
            """
            SELECT e.person_id, e.organization_id, e.role_id, e.start_date, e.end_date,
                   o.name AS organization_name, r.title AS role_title
            FROM employment_record e
            JOIN organization o ON o.organization_id = e.organization_id
            JOIN role r ON r.role_id = e.role_id
            ORDER BY e.start_date, e.employment_id
            """
        )
        jobs = list(cur.fetchall())

    certs: dict[int, set[int]] = {}
    for row in cert_rows:
        certs.setdefault(row["person_id"], set()).add(row["certification_id"])

    assets: dict[int, dict[int, int]] = {}
    for row in asset_rows:
        assets.setdefault(row["person_id"], {})[row["asset_type_id"]] = row["quantity"]

    employment: dict[int, list[dict]] = {}
    for row in jobs:
        employment.setdefault(row["person_id"], []).append(
            {
                "organization_id": row["organization_id"],
                "role_id": row["role_id"],
                "start_date": as_date(row["start_date"]),
                "end_date": as_date(row["end_date"]),
                "organization_name": row["organization_name"],
                "role_title": row["role_title"],
            }
        )

    profiles = []
    for person in people:
        profiles.append(
            {
                "person_id": person["person_id"],
                "full_name": person["full_name"],
                "age": person["age"],
                "certification_ids": certs.get(person["person_id"], set()),
                "assets": assets.get(person["person_id"], {}),
                "employment": employment.get(person["person_id"], []),
            }
        )

