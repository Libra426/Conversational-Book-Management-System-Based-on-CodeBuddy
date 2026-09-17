# API / 服务接口规范

采用 REST API。权限通过请求头 `X-Role`（reader/librarian/admin）与 `X-User-Id` 表达。

## 1. 读者与借阅证

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/readers` | 公开 | 注册读者 |
| GET | `/api/readers/{id}` | reader(本人)/librarian/admin | 查询读者 |
| POST | `/api/admin/borrow-cards` | admin | 办理借阅证 |
| DELETE | `/api/admin/borrow-cards/{card_no}` | admin | 注销借阅证 |

## 2. 图书与馆藏

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| GET | `/api/catalog/books?title=&author=&isbn=` | reader | 查询图书 |
| POST | `/api/admin/book-titles` | admin | 添加标题 |
| DELETE | `/api/admin/book-titles/{id}` | admin | 删除标题 |
| POST | `/api/admin/library-items` | admin | 添加副本 |
| DELETE | `/api/admin/library-items/{barcode}` | admin | 移除副本 |

## 3. 借还与查询

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/circulation/borrow` | librarian | 办理借书 |
| POST | `/api/circulation/return` | librarian | 办理还书 |
| GET | `/api/readers/{id}/loans` | reader(本人)/librarian | 查询借阅信息 |

## 4. 预约

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/reservations` | reader | 预约图书 |
| GET | `/api/readers/{id}/reservations` | reader(本人) | 查询预约 |

## 5. 规则维护

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/admin/borrow-policies` | admin | 新增/更新借阅规则 |
| POST | `/api/admin/fine-rules` | admin | 新增/更新罚款规则 |

## 6. 关键接口详情

### POST /api/circulation/borrow（办理借书）

- 请求：`{ "card_no": "1", "barcode": "BC-1001" }`
- 成功：201 `{ id, reader_id, item_id, due_date, status }`
- 失败：403 借阅证无效；409 超出借阅数量 / 存在超期未还 / 图书不可借

### POST /api/circulation/return（办理还书）

- 请求：`{ "barcode": "B0001" }`
- 成功：200 `{ loan_id, returned_at, fine: {overdue_days, amount} | null }`
- 失败：404 非本馆藏书 / 未找到借阅记录

### POST /api/reservations（预约图书）

- 请求：`{ "reader_id": 1, "title_id": 1 }`
- 成功：201 `{ id, reader_id, title_id, status, created_at }`
- 失败：404 读者/标题不存在；409 重复预约
