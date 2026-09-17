"""预约测试（TC-012/013 + 分支）。"""
from tests.helpers import add_title, register_reader


def test_reserve_success(client):
    reader = register_reader(client)
    title = add_title(client)
    resp = client.post(
        "/api/reservations", json={"reader_id": reader["id"], "title_id": title["id"]}
    )
    assert resp.status_code == 201
    assert resp.json()["status"] == "ACTIVE"


def test_reserve_duplicate(client):
    reader = register_reader(client)
    title = add_title(client)
    payload = {"reader_id": reader["id"], "title_id": title["id"]}
    client.post("/api/reservations", json=payload)
    resp = client.post("/api/reservations", json=payload)
    assert resp.status_code == 409
    assert resp.json()["code"] == "DUPLICATE_RESERVATION"


def test_reserve_reader_not_found(client):
    title = add_title(client)
    resp = client.post(
        "/api/reservations", json={"reader_id": 999, "title_id": title["id"]}
    )
    assert resp.status_code == 404
    assert resp.json()["code"] == "READER_NOT_FOUND"


def test_reserve_title_not_found(client):
    reader = register_reader(client)
    resp = client.post(
        "/api/reservations", json={"reader_id": reader["id"], "title_id": 999}
    )
    assert resp.status_code == 404
    assert resp.json()["code"] == "TITLE_NOT_FOUND"
