from datetime import date

from app.services.qualification import (
    evaluate_all,
    evaluate_requirement,
    years_experience,
)


def person(**overrides):
    profile = {
        "person_id": 1,
        "full_name": "Test Applicant",
        "age": 30,
        "certification_ids": set(),
        "assets": {},
        "employment": [],
    }
    profile.update(overrides)
    return profile


def test_min_age_experience_license_ownership_and_prior_agency():
    today = date(2026, 11, 5)
    profile = person(
        age=24,
        certification_ids={3},
        assets={2: 1},
        employment=[
            {
                "organization_id": 8,
                "start_date": date(2024, 1, 1),
                "end_date": None,
            }
        ],
    )
    age = {
        "code": "min_age",
        "minimum_value": 21,
        "asset_name": None,
        "certification_name": None,
        "history_organization_name": None,
    }
    license_rule = {
        "code": "has_certification",
        "certification_id": 3,
        "certification_name": "First Aid",
        "minimum_value": None,
        "asset_name": None,
        "history_organization_name": None,
    }
    missing_license = {**license_rule, "certification_id": 9, "certification_name": "Notary"}
    ownership = {
        "code": "min_ownership",
        "asset_type_id": 2,
        "minimum_value": 2,
        "asset_name": "Filing Cabinet",
        "certification_name": None,
        "history_organization_name": None,
    }
    prior = {
        "code": "prior_agency",
        "history_organization_id": 8,
        "history_organization_name": "Office of Hallway Passes",
        "minimum_value": None,
        "asset_name": None,
        "certification_name": None,
    }
    experience = {
        "code": "min_experience",
        "minimum_value": 2,
        "asset_name": None,
        "certification_name": None,
        "history_organization_name": None,
    }

    assert evaluate_requirement(age, profile, today)[0] is True
    assert evaluate_requirement({**age, "minimum_value": 40}, profile, today)[0] is False
    assert evaluate_requirement(license_rule, profile, today)[0] is True
    assert evaluate_requirement(missing_license, profile, today)[0] is False
    assert evaluate_requirement(ownership, profile, today)[0] is False
    assert evaluate_requirement(prior, profile, today)[0] is True
    assert evaluate_requirement(
        {**prior, "history_organization_id": 1}, profile, today
    )[0] is False
    assert evaluate_requirement(experience, profile, today)[0] is True


def test_open_job_counts_through_the_given_day():
    jobs = [{"start_date": date(2020, 1, 1), "end_date": None}]
    assert years_experience(jobs, date(2022, 1, 1)) == (date(2022, 1, 1) - date(2020, 1, 1)).days / 365


def test_missing_asset_counts_as_zero():
    profile = person()
    passed, label = evaluate_requirement(
        {
            "code": "min_ownership",
            "asset_type_id": 4,
            "minimum_value": 1,
            "asset_name": "Desk Lamp",
        },
        profile,
        date(2026, 11, 5),
    )
    assert passed is False
    assert "Desk Lamp" in label


def test_every_rule_must_pass():
    profile = person(age=40, certification_ids={1})
    requirements = [
        {"code": "min_age", "minimum_value": 21},
        {
            "code": "has_certification",
            "certification_id": 2,
            "certification_name": "Forklift",
        },
    ]
    qualified, failed = evaluate_all(requirements, profile, today=date(2026, 11, 5))
    assert qualified is False
    assert failed == ["Hold a Forklift license"]
