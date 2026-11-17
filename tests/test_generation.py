import random

from app.services.generation import AGE_OPTIONS, build_starting_requirements


def catalog():
    return {
        "organizations": [
            {"organization_id": index, "name": f"Office {index}"} for index in range(1, 5)
        ],
        "roles": [{"role_id": index, "title": f"Role {index}"} for index in range(1, 5)],
        "certifications": [
            {"certification_id": 1, "name": "Notary"},
            {"certification_id": 2, "name": "Forklift"},
        ],
        "assets": [
            {"asset_type_id": 1, "name": "Rubber Stamp"},
            {"asset_type_id": 2, "name": "Desk Lamp"},
        ],
    }


def test_each_agency_and_position_starts_with_one_rule():
    specs = build_starting_requirements(catalog(), random.Random(2))
    assert len(specs) == 8
    org_ids = sorted(spec["organization_id"] for spec in specs if spec["organization_id"])
    role_ids = sorted(spec["role_id"] for spec in specs if spec["role_id"])
    assert org_ids == [1, 2, 3, 4]
    assert role_ids == [1, 2, 3, 4]
    for spec in specs:
        assert (spec["organization_id"] is None) ^ (spec["role_id"] is None)
        if spec["code"] == "min_age":
            assert spec["minimum_value"] in AGE_OPTIONS
            assert spec["asset_type_id"] is None
            assert spec["certification_id"] is None
            assert spec["history_organization_id"] is None
        elif spec["code"] == "min_ownership":
            assert spec["minimum_value"] in (1, 2, 3)
            assert spec["asset_type_id"] in (1, 2)
            assert spec["certification_id"] is None
        elif spec["code"] == "has_certification":
            assert spec["certification_id"] in (1, 2)
            assert spec["minimum_value"] is None
            assert spec["asset_type_id"] is None
        elif spec["code"] == "prior_agency":
            assert spec["history_organization_id"] in (1, 2, 3, 4)
            assert spec["minimum_value"] is None
        elif spec["code"] == "min_experience":
            assert spec["minimum_value"] in (1, 2, 3, 4, 5)
            assert spec["certification_id"] is None
        else:
            raise AssertionError(spec["code"])


def test_request_sentence_uses_the_and_an_article():
    from app.services.gameplay import request_sentence

    assert (
        request_sentence("Bureau of Parking", "Archivist")
        == "I want to work for The Bureau of Parking as an Archivist."
    )
    assert (
        request_sentence("Office of Lost Staplers", "Clerk")
        == "I want to work for The Office of Lost Staplers as a Clerk."
    )
