"""借还集成测试（TC-003~TC-010、TC-011）。"""
from datetime import date, timedelta

from app.domain.models import Loan
from tests.helpers import (
    LIBRARIAN,
    add_item,
    add_title,
    issue_card,
    register_reader,
)


def _setup(client, barcode="B0"):
    reader = register_reader(client)
    card = issue_card(client, reader["id"])
    title = add_title(client)
    item = add_item(client, title["id"], barcode)
    return reader, card, title, item


def test_borrow_success(client):
    reader, card, _, _ = _setup(client)
    resp = client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers=LIBRARIAN,
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["status"] == "BORROWED"
    assert body["reader_id"] == reader["id"]


def test_borrow_invalid_card(client):
    resp = client.post(
        "/api/circulation/borrow",
        json={"card_no": "NOPE", "barcode": "B0"},
        headers=LIBRARIAN,
    )
    assert resp.status_code == 403
    assert resp.json()["code"] == "INVALID_CARD"


def test_borrow_too_many(client):
    reader = register_reader(client)  # 本科生最多 5 本
    card = issue_card(client, reader["id"])
    title = add_title(client)
    for i in range(5):
        add_item(client, title["id"], f"B{i}")
        resp = client.post(
            "/api/circulation/borrow",
            json={"card_no": card["card_no"], "barcode": f"B{i}"},
            headers=LIBRARIAN,
        )
        assert resp.status_code == 201
    add_item(client, title["id"], "B5")
    resp = client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B5"},
        headers=LIBRARIAN,
    )
    assert resp.status_code == 409
    assert resp.json()["code"] == "TOO_MANY_LOANS"


def test_borrow_overdue_loan(client, db):
    reader, card, title, _ = _setup(client, "B0")
    client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers=LIBRARIAN,
    )
    loan = db.query(Loan).first()
    loan.due_date = date.today() - timedelta(days=1)
    db.commit()

    add_item(client, title["id"], "B1")
    resp = client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B1"},
        headers=LIBRARIAN,
    )
    assert resp.status_code == 409
    assert resp.json()["code"] == "OVERDUE_LOAN"


def test_borrow_item_not_available(client):
    reader, card, _, _ = _setup(client)
    client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers=LIBRARIAN,
    )
    resp = client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers=LIBRARIAN,
    )
    assert resp.status_code == 409
    assert resp.json()["code"] == "ITEM_NOT_BORROWABLE"


def test_return_success(client):
    reader, card, _, _ = _setup(client)
    client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers=LIBRARIAN,
    )
    resp = client.post(
        "/api/circulation/return", json={"barcode": "B0"}, headers=LIBRARIAN
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["fine"] is None
    assert body["returned_at"] is not None


def test_return_item_not_found(client):
    resp = client.post(
        "/api/circulation/return", json={"barcode": "NOPE"}, headers=LIBRARIAN
    )
    assert resp.status_code == 404
    assert resp.json()["code"] == "ITEM_NOT_FOUND"


def test_return_overdue_generates_fine(client, db):
    reader, card, _, _ = _setup(client)
    client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers=LIBRARIAN,
    )
    loan = db.query(Loan).first()
    loan.due_date = date.today() - timedelta(days=5)
    db.commit()

    resp = client.post(
        "/api/circulation/return", json={"barcode": "B0"}, headers=LIBRARIAN
    )
    assert resp.status_code == 200
    fine = resp.json()["fine"]
    assert fine is not None
    assert fine["overdue_days"] == 5
    assert fine["amount"] == 0.5  # 中文图书 0.10/天 × 5 天


def test_query_loans_success(client):
    reader, card, _, _ = _setup(client)
    client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers=LIBRARIAN,
    )
    resp = client.get(
        f"/api/readers/{reader['id']}/loans",
        headers={"X-Role": "reader", "X-User-Id": str(reader["id"])},
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 1
