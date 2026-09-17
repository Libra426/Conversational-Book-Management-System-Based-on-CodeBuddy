# 架构设计

## 1. 架构风格

采用**分层架构 + MVC**，技术栈 FastAPI + SQLAlchemy + SQLite。

```
presentation（routers/Controller 层）
        │ 调用
        ▼
application（services 应用服务层）
        │ 编排用例流程
        ▼
domain（领域实体 + 策略，纯业务）
        ▲
infrastructure（repositories + database 持久化）
```

## 2. 各层职责

| 层 | 目录 | 职责 |
|---|---|---|
| Presentation | `app/routers/` | 接收 HTTP 请求、参数校验（Pydantic schema）、调用应用服务、返回 DTO；不写业务规则 |
| Application | `app/services/` | 组织用例流程、事务边界、权限调用 |
| Domain | `app/domain/` | 领域实体（Reader/BookTitle/LibraryItem/Loan/Reservation/…）与策略（BorrowPolicy/FineRule） |
| Infrastructure | `app/repositories/` + `database.py` | 持久化、Repository 实现、DB 会话 |
| DTO | `app/schemas/` | 接口入参/出参模型，隔离接口层与领域层 |

## 3. 主要模块

| 模块 | 职责 |
|---|---|
| reader | 读者注册、借阅证 |
| catalog | 图书标题、馆藏副本 |
| circulation | 借书、还书、借阅查询 |
| reservation | 预约 |
| fine | 罚款计算、罚单 |
| admin | 管理员维护、规则维护 |

## 4. 权限控制策略

- 接口层通过请求头 `X-Role`（reader/librarian/admin）与 `X-User-Id` 标识操作人。
- `app/deps.py` 提供 `require_role(...)` 依赖注入，校验失败返回 403。
- 读者只能查本人借阅信息；图书管理员可查任意读者；系统管理员独占管理接口。

## 5. 异常处理策略

- 领域异常统一继承 `DomainError`，携带语义化 `code` 与 HTTP 状态码。
- 全局异常处理器把 `DomainError` 映射为统一 JSON：`{detail, code}`。

## 6. 事务边界

- 借书、还书、办证等“多实体写操作”在应用服务内以单一 DB 会话完成，失败即回滚。

## 7. 业务规则放置

- 借阅数量/期限 → `BorrowPolicy`（策略表 borrow_policies）+ `policy_service`。
- 罚款计算 → `FineRule`（策略表 fine_rules）+ `fine_service`。
- 借/还流程编排 → `CirculationService`。

## 8. 设计模式

| 模式 | 位置 |
|---|---|
| Strategy | BorrowPolicy（按读者类型）、FineRule（按借出物类型） |
| Repository | `app/repositories/*` 抽象持久化 |
| Service Layer | `app/services/*` 组织用例 |
| DTO | `app/schemas/*` 隔离接口与领域 |
| MVC | routers(Controller) / domain+services(Model) / schemas(View 数据) |
