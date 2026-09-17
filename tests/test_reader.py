"""读者与借阅证测试（TC-001/002 + 分支）。"""
from datetime import datetime

from tests.helpers import ADMIN, issue_card, register_reader


def test_register_reader_success(client):
    reader = register_reader(client)
    assert reader["id"] == 1
    assert reader["reader_type"] == "UNDERGRADUATE"


def test_issue_card_success(client):
    reader = register_reader(client)
    card = issue_card(client, reader["id"])
    # BR-002：证号格式 `CARD` + 4 位年份 + 6 位序号
    assert card["card_no"] == f"CARD{datetime.now().year}000001"
    assert card["reader_id"] == reader["id"]
    assert card["status"] == "ACTIVE"


def test_issue_card_inlines_reader_info(client):
    reader = register_reader(client, name="李四")
    card = issue_card(client, reader["id"])
    assert card["reader_name"] == "李四"
    assert card["department"] == "计算机学院"


def test_issue_card_reader_not_found(client):
    resp = client.post(
        "/api/admin/borrow-cards", json={"reader_id": 999}, headers=ADMIN
    )
    assert resp.status_code == 404
    assert resp.json()["code"] == "READER_NOT_FOUND"


def test_issue_card_duplicate(client):
    reader = register_reader(client)
    issue_card(client, reader["id"])
    resp = client.post(
        "/api/admin/borrow-cards", json={"reader_id": reader["id"]}, headers=ADMIN
    )
    assert resp.status_code == 409
    assert resp.json()["code"] == "DUPLICATE_CARD"


def test_get_reader_by_card(client):
    reader = register_reader(client, name="李四")
    card = issue_card(client, reader["id"])
    resp = client.get(f"/api/readers/by-card/{card['card_no']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == reader["id"]
    assert resp.json()["name"] == "李四"


def test_get_reader_by_card_not_found(client):
    resp = client.get("/api/readers/by-card/NOPE")
    assert resp.status_code == 404
    assert resp.json()["code"] == "NOT_FOUND"
