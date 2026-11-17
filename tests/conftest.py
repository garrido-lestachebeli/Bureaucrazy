import os

import pytest

os.environ["MYSQL_DATABASE"] = "bureaucrazy_test"


@pytest.fixture(scope="session")
def database():
    from app.database_setup import can_connect, reset_database

    if not can_connect():
        pytest.skip("MySQL is not reachable with the settings in .env")
    reset_database("bureaucrazy_test")
    yield
