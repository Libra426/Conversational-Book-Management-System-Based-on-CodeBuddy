"""测试辅助：通过 API 快速构造领域对象。"""

ADMIN = {"X-Role": "admin", "X-User-Id": "1"}
LIBRARIAN = {"X-Role": "librarian", "X-User-Id": "1"}


def register_reader(client, name="张三", reader_type="UNDERGRADUATE"):
    resp = client.post(
        "/api/readers",
        json={"name": name, "department": "计算机学院", "reader_type": reader_type},
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def issue_card(client, reader_id):
    resp = client.post(
        "/api/admin/borrow-cards",
        json={"reader_id": reader_id},
        headers=ADMIN,
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def add_title(client, title="软件工程", isbn="ISBN0001", item_type="CHINESE_BOOK"):
    resp = client.post(
        "/api/admin/book-titles",
        json={"title": title, "author": "作者", "isbn": isbn, "item_type": item_type},
        headers=ADMIN,
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def add_item(client, title_id, barcode):
    resp = client.post(
        "/api/admin/library-items",
        json={"title_id": title_id, "barcode": barcode},
        headers=ADMIN,
    )
    assert resp.status_code == 201, resp.text
    return resp.json()
