import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)

    def override():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def register(c, name="alice", pw="secret1"):
    return c.post("/api/users", json={"username": name, "password": pw})


def test_register_and_duplicate(client):
    r = register(client)
    assert r.status_code == 201 and r.json()["username"] == "alice"
    assert "password" not in r.text
    assert register(client).status_code == 409
    assert client.post("/api/users", json={"username": "ab", "password": "x"}).status_code == 422


def test_candidates(client):
    r = client.post("/api/candidates", json={"name": "  Bob "})
    assert r.status_code == 201 and r.json()["name"] == "Bob"
    assert client.post("/api/candidates", json={"name": "Bob"}).status_code == 409
    assert client.post("/api/candidates", json={"name": "   "}).status_code == 422
    assert [c["name"] for c in client.get("/api/candidates").json()] == ["Bob"]
    assert client.get("/api/votes/candidates").json() == client.get("/api/candidates").json()


def test_vote_requires_auth(client):
    cid = client.post("/api/candidates", json={"name": "Bob"}).json()["id"]
    assert client.post(f"/api/votes?candidateId={cid}").status_code == 401
    register(client)
    assert client.post(f"/api/votes?candidateId={cid}", auth=("alice", "wrong")).status_code == 401


def test_vote_flow_and_results(client):
    a = client.post("/api/candidates", json={"name": "A"}).json()["id"]
    b = client.post("/api/candidates", json={"name": "B"}).json()["id"]
    client.post("/api/candidates", json={"name": "C"})
    register(client, "alice")
    register(client, "bob")

    r = client.post(f"/api/votes?candidateId={b}", auth=("alice", "secret1"))
    assert r.status_code == 201
    assert r.json()["candidateId"] == b and r.json()["userId"] == 1
    # second vote by same user is rejected
    assert client.post(f"/api/votes?candidateId={a}", auth=("alice", "secret1")).status_code == 409
    assert client.post(f"/api/votes?candidateId={b}", auth=("bob", "secret1")).status_code == 201

    res = client.get("/api/votes/results").json()
    assert [(x["name"], x["votes"]) for x in res] == [("B", 2), ("A", 0), ("C", 0)]


def test_vote_for_unknown_candidate(client):
    register(client)
    r = client.post("/api/votes?candidateId=999", auth=("alice", "secret1"))
    assert r.status_code == 404
    # failed attempt must not use up the user's vote
    cid = client.post("/api/candidates", json={"name": "A"}).json()["id"]
    assert client.post(f"/api/votes?candidateId={cid}", auth=("alice", "secret1")).status_code == 201
