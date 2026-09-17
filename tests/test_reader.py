"""读者与借阅证测试（TC-001/002 + 分支）。"""
from tests.helpers import ADMIN, issue_card, register_reader


def test_register_reader_success(client):
    reader = register_reader(client)
    assert reader["id"] == 1
    assert reader["reader_type"] == "UNDERGRADUATE"


def test_issue_card_success(client):
    reader = register_reader(client)
    card = issue_card(client, reader["id"])
    assert card["card_no"] == "1"
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
