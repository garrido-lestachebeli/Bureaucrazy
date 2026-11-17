# Bureaucrazy

You are the clerk. Each request is one sentence: "I want to work for The [organization] as a [role]." The applicant file and the posted rules come from MySQL. Approve people who meet every rule for that agency and that role. Deny the rest.

The game is backed by a MySQL database. World tables hold agencies, roles, licenses, assets, applicants, and each applicant's licenses, assets, and work history. Game tables hold each game, the rules it posts, the request currently on the desk, and every request the player has judged. A FastAPI service connects to the database; it currently exposes a health check.
<<<<<<< HEAD

Rules can ask for a minimum age, a license, a minimum number of an asset, past work at an agency, or a minimum number of years of work experience. Overlapping jobs count toward experience separately.
=======
>>>>>>> 49213216522404a652c6196f1b9dc65bc7089432

## Layout

- `database/schema.sql` — world tables, game tables, and the open case on the desk
- `database/seed_world.sql` — agencies, roles, licenses, assets, applicants, and requirement types
<<<<<<< HEAD
- `backend/app` — FastAPI service. SQL lives in `repositories`. Rules live in `services`. Routes live in `routers`.
- `tests` — rule checks, and database checks against a separate test database
=======
- `backend/app` — FastAPI service. SQL lives in `repositories`. Routes live in `routers`.
- `tests` — database checks against a separate test database
>>>>>>> 49213216522404a652c6196f1b9dc65bc7089432
- `scripts/init_db.py` — creates the database and loads the world data
- `scripts/start_dev_mysql.ps1` — starts a second MySQL server on port 3307

## Setup

MySQL 8 must be running. This project expects a local server on port 3306.

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set `MYSQL_PASSWORD` to the local MySQL password. `.env` is not committed.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
python scripts\init_db.py
```

`init_db.py` drops and recreates the database named in `MYSQL_DATABASE`, so only point it at a database that can be thrown away. The name must start with `bureaucrazy`.

Start the API:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --app-dir backend --port 8001
```

http://127.0.0.1:8001/api/health returns `{"status": "ok"}` when the API can reach MySQL. Port 8000 is left alone because other local programs often use it.

## If the course MySQL login is rejected

Root on port 3306 may require a password this repo does not store. A second server on port 3307 leaves the MySQL80 service alone:

```powershell
.\scripts\start_dev_mysql.ps1
```

Set `MYSQL_PORT=3307` and leave `MYSQL_PASSWORD` empty in `.env`, then run `python scripts\init_db.py` once. The data directory lives under your temp folder, so start that script again after a reboot.

## Tests

```powershell
.\.venv\Scripts\Activate.ps1
pytest
```

<<<<<<< HEAD
Rule tests always run. Database tests use a separate `bureaucrazy_test` database and are skipped when MySQL rejects the login in `.env`.
=======
Tests use a separate `bureaucrazy_test` database and are skipped when MySQL rejects the login in `.env`.
>>>>>>> 49213216522404a652c6196f1b9dc65bc7089432
