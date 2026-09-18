# API / 服务接口规范

采用 REST API。权限通过请求头 `X-Role`（reader/librarian/admin）与 `X-User-Id` 表达；`/docs` 中也支持 HTTP Bearer 令牌（令牌即角色，如 `admin:1`，优先于请求头）。

> 说明：`GET /api/catalog/books`、`GET /api/readers/by-card/{card_no}` 为公开端点；`POST /api/reservations` 由读者调用（请求体携带 reader_id），当前未做服务端身份校验，属实验简化。

## 1. 读者与借阅证

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/readers` | 公开 | 注册读者 |
| GET | `/api/readers` | librarian/admin | 读者列表 |
| GET | `/api/readers/by-card/{card_no}` | 公开 | 借阅证号查询读者 |
| GET | `/api/readers/{id}` | reader(本人)/librarian/admin | 查询读者 |
| POST | `/api/admin/borrow-cards` | admin | 办理借阅证 |
| GET | `/api/admin/borrow-cards` | admin | 借阅证列表 |
| DELETE | `/api/admin/borrow-cards/{card_no}` | admin | 注销借阅证 |

## 2. 图书与馆藏

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| GET | `/api/catalog/books?title=&author=&isbn=` | 公开 | 查询图书 |
| POST | `/api/admin/book-titles` | admin | 添加标题 |
| DELETE | `/api/admin/book-titles/{id}` | admin | 删除标题 |
| POST | `/api/admin/library-items` | admin | 添加副本 |
| DELETE | `/api/admin/library-items/{barcode}` | admin | 移除副本 |

## 3. 借还与查询

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/circulation/borrow` | librarian | 办理借书 |
| POST | `/api/circulation/return` | librarian | 办理还书 |
| GET | `/api/readers/{id}/loans` | reader(本人)/librarian/admin | 查询借阅信息 |

## 4. 预约

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| POST | `/api/reservations` | reader | 预约图书 |
| GET | `/api/readers/{id}/reservations` | reader(本人)/librarian/admin | 查询预约 |

## 5. 规则与人员维护

| 方法 | 路径 | 权限 | 说明 |
|---|---|---|---|
| GET | `/api/admin/borrow-policies` | admin | 借阅规则列表 |
| POST | `/api/admin/borrow-policies` | admin | 新增/更新借阅规则 |
| GET | `/api/admin/fine-rules` | admin | 罚款规则列表 |
| POST | `/api/admin/fine-rules` | admin | 新增/更新罚款规则 |
| GET | `/api/admin/librarians` | admin | 图书管理员列表 |
| POST | `/api/admin/librarians` | admin | 添加图书管理员 |
| DELETE | `/api/admin/librarians/{id}` | admin | 删除图书管理员 |
| GET | `/api/admin/system-admins` | admin | 系统管理员列表 |
| POST | `/api/admin/system-admins` | admin | 添加系统管理员 |
| DELETE | `/api/admin/system-admins/{id}` | admin | 删除系统管理员 |

## 6. 关键接口详情

### POST /api/circulation/borrow（办理借书）

- 请求：`{ "card_no": "CARD2026000001", "barcode": "BC-1001" }`
- 成功：201 `{ id, reader_id, item_id, barcode, title, author, item_type, borrowed_at, due_date, returned_at, status }`
- 失败：403 借阅证无效；409 超出借阅数量 / 存在超期未还 / 图书不可借；404 非本馆藏书

### POST /api/circulation/return（办理还书）

- 请求：`{ "barcode": "BC-1001" }`
- 成功：200 `{ loan_id, returned_at, fine: {overdue_days, amount} | null }`
- 失败：404 非本馆藏书 / 未找到借阅记录

### POST /api/reservations（预约图书）

- 请求：`{ "reader_id": 1, "title_id": 1 }`
- 成功：201 `{ id, reader_id, title_id, book_title, author, item_type, status, created_at }`
- 失败：404 读者/标题不存在；409 重复预约
