# Online Voting System (FastAPI)

A small voting API, converted from Spring Boot to Python/FastAPI.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive docs.

Config: set `DATABASE_URL` (see `.env.example`). Default is a local SQLite file;
for MySQL install `pymysql` and use `mysql+pymysql://user:pass@localhost:3306/vote`.
Tables are created automatically at startup.

## Endpoints

| Method | Path | Notes |
|---|---|---|
| POST | `/api/users` | register `{"username","password"}` |
| GET / POST | `/api/candidates` | list / add `{"name"}` |
| GET | `/api/votes/candidates` | candidates to vote for |
| POST | `/api/votes?candidateId=1` | cast vote; needs HTTP Basic login; one vote per user |
| GET | `/api/votes/results` | votes per candidate, highest first |

## Tests

```bash
pytest
```

## Bugs fixed compared with the Spring version

- DB password was committed in `application.properties` -> now `DATABASE_URL` env var.
- Every vote was saved as user 1 -> votes now belong to the logged-in user.
- Users could vote unlimited times -> one vote per user (checked in code and by a DB unique constraint).
- Votes for non-existent candidates were accepted -> 404.
- `/results` returned raw vote rows -> now returns a tally per candidate.
- `User` had no endpoints and would have stored plain-text passwords -> registration with salted PBKDF2 hashes.
- Blank / duplicate candidate names were allowed -> validated (422 / 409).
