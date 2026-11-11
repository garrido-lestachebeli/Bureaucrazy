# Bureaucrazy

You are the clerk. Each request is one sentence: "I want to work for The [organization] as a [role]." The applicant file and the posted rules come from MySQL. Approve people who meet every rule for that agency and that role. Deny the rest.

The game is backed by a MySQL database that holds the world: agencies, roles, licenses, assets, applicants, and each applicant's licenses, assets, and work history. Python scripts create the database and load that data.

## Layout

- `database/schema.sql` — the world tables
- `database/seed_world.sql` — agencies, roles, licenses, assets, and applicants
- `backend/app` — Python package. `config.py` reads `.env`, `db.py` opens connections, and `database_setup.py` rebuilds the database from the SQL files.
- `scripts/init_db.py` — creates the database and loads the world data

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
