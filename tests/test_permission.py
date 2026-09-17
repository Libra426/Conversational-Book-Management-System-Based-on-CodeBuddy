"""权限测试（TC-014）。"""
from tests.helpers import add_item, add_title, issue_card, register_reader


def test_reader_cannot_execute_admin_operation(client):
    reader = register_reader(client)
    resp = client.post(
        "/api/admin/borrow-cards",
        json={"reader_id": reader["id"]},
        headers={"X-Role": "reader", "X-User-Id": str(reader["id"])},
    )
    assert resp.status_code == 403


def test_reader_cannot_borrow(client):
    reader = register_reader(client)
    card = issue_card(client, reader["id"])
    title = add_title(client)
    add_item(client, title["id"], "B0")
    resp = client.post(
        "/api/circulation/borrow",
        json={"card_no": card["card_no"], "barcode": "B0"},
        headers={"X-Role": "reader", "X-User-Id": str(reader["id"])},
    )
    assert resp.status_code == 403


def test_reader_cannot_query_others(client):
    reader1 = register_reader(client, name="甲")
    reader2 = register_reader(client, name="乙")
    resp = client.get(
        f"/api/readers/{reader2['id']}/loans",
        headers={"X-Role": "reader", "X-User-Id": str(reader1["id"])},
    )
    assert resp.status_code == 403
    assert resp.json()["code"] == "PERMISSION_DENIED"


def test_reader_cannot_query_other_reader_info(client):
    reader1 = register_reader(client, name="甲")
    reader2 = register_reader(client, name="乙")
    resp = client.get(
        f"/api/readers/{reader2['id']}",
        headers={"X-Role": "reader", "X-User-Id": str(reader1["id"])},
    )
    assert resp.status_code == 403


def test_reader_can_query_own_info(client):
    reader = register_reader(client)
    resp = client.get(
        f"/api/readers/{reader['id']}",
        headers={"X-Role": "reader", "X-User-Id": str(reader["id"])},
    )
    assert resp.status_code == 200
    assert resp.json()["name"] == "张三"


def test_bearer_token_grants_admin(client):
    reader = register_reader(client)
    resp = client.post(
        "/api/admin/borrow-cards",
        json={"reader_id": reader["id"]},
        headers={"Authorization": "Bearer admin"},
    )
    assert resp.status_code == 201


def test_bearer_token_wrong_role_denied(client):
    reader = register_reader(client)
    resp = client.post(
        "/api/admin/borrow-cards",
        json={"reader_id": reader["id"]},
        headers={"Authorization": "Bearer reader"},
    )
    assert resp.status_code == 403


def test_bearer_token_overrides_header(client):
    reader = register_reader(client)
    resp = client.post(
        "/api/admin/borrow-cards",
        json={"reader_id": reader["id"]},
        headers={"Authorization": "Bearer admin", "X-Role": "reader"},
    )
    assert resp.status_code == 201
