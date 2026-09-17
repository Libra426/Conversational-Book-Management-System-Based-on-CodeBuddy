# 图书管理系统（AI 时代 Spec-Driven 实验）

《软件设计与体系结构》课程实验：图书管理系统的 Spec-Driven 架构设计、详细设计与 Agent 辅助实现。

## 1. 技术栈

- Python 3.13 + FastAPI + SQLAlchemy 2 + SQLite + Pydantic 2 + pytest

## 2. 架构

分层架构 + MVC：

```
presentation（app/routers）→ application（app/services）→ domain（app/domain）
                                        ↕
                              infrastructure（app/repositories + database）
```

- Strategy 模式：`BorrowPolicyService`（按读者类型）、`FineService`（按借出物类型）
- Repository 模式：`app/repositories/*`
- DTO 隔离：`app/schemas/*`

## 3. 目录结构

```
library-management-ai/
  specs/             # 21 份 Spec 文档 + 开发宪法 + 5 张 PlantUML 图
  app/
    routers/         # 表现层（Controller）
    services/        # 应用服务层
    domain/          # 领域实体 + 枚举 + 策略
    repositories/    # 基础设施层（持久化）
    schemas/         # DTO
  tests/             # pytest 测试
```

## 4. 启动方式

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

启动后访问 http://127.0.0.1:8000/docs 查看交互式 API 文档。

## 5. 测试方式

```bash
pytest -v
```

## 6. 权限模型

通过请求头表达操作人：

- `X-Role`: `reader` / `librarian` / `admin`
- `X-User-Id`: 操作人 id

在 `/docs` 里更简单：点右上角 **Authorize** 按钮，粘贴角色（`admin` / `librarian` / `reader`，可带用户 id 如 `admin:1`）即可全局生效。Bearer 令牌优先于 `X-Role` 头。

> **读者身份说明**：借阅证号（`card_no`）对外，读者内部 id（`reader_id`）仅作数据库主键。读者登录、查借阅、预约、借书均使用借阅证号——读者前端用 `GET /api/readers/by-card/{card_no}` 把证号解析成内部读者 id，再携带 `X-User-Id` 调用借阅/预约接口。

## 7. 核心用例

- 读者：注册、查询图书、查询本人借阅信息、预约图书
- 图书管理员：办理借书、办理还书、查询任意读者借阅信息
- 系统管理员：办理/注销借阅证、维护标题/馆藏/管理员/借阅与罚款规则

## 8. 核心 API

```
POST /api/readers                        注册读者
POST /api/admin/borrow-cards             办理借阅证
POST /api/admin/book-titles              添加标题
POST /api/admin/library-items            添加馆藏副本
GET  /api/catalog/books                  查询图书
POST /api/circulation/borrow             办理借书（librarian）
POST /api/circulation/return             办理还书（librarian）
GET  /api/readers/{id}/loans             查询借阅信息
GET  /api/readers/by-card/{card_no}      借阅证号登录（读者）
POST /api/reservations                   预约图书
```

## 9. 借阅与罚款规则

| 读者类型 | 上限 | 期限 |
|---|---|---|
| 专科生 | 3 | 30 天 |
| 本科生 | 5 | 30 天 |
| 研究生 | 10 | 60 天 |
| 博士生 | 15 | 90 天 |
| 教师 | 20 | 90 天 |

| 借出物类型 | 罚款（元/天） |
|---|---|
| 中文图书 | 0.10 |
| 外文图书 | 0.20 |
| 中文杂志 | 0.05 |
| 外文杂志 | 0.10 |
| 论文 | 0.50 |

## 10. 演示数据（开箱即用）

首次启动自动写入以下演示数据，可直接测试借还书：

**借阅证**

| 借阅证号 | 读者 | 类型 | 上限 / 期限 |
|---|---|---|---|
| CARD2026000001 | 张三 | 本科生 | 5 本 / 30 天 |
| CARD2026000002 | 李四 | 研究生 | 10 本 / 60 天 |
| CARD2026000003 | 王五 | 教师 | 20 本 / 90 天 |

**馆藏副本（条码）**

| 条码 | 书名 | 类型 |
|---|---|---|
| BC-1001 / BC-1002 / BC-1003 | 软件工程 | 中文图书 |
| BC-2001 / BC-2002 | 算法导论 | 外文图书 |
| BC-3001 | 计算机学报 | 中文杂志 |
| BC-4001 / BC-4002 | Nature | 外文杂志 |
| BC-5001 | 基于深度学习的图像识别研究 | 论文 |

在 `/docs` 右上角 Authorize 填 `librarian`，然后：

- 借书：`POST /api/circulation/borrow` → `{"card_no": "CARD2026000001", "barcode": "BC-1001"}`
- 还书：`POST /api/circulation/return` → `{"barcode": "BC-1001"}`

超期还书会自动按类型生成罚款（如中文图书 0.10 元/天）。

## 11. UML 文档

见 `specs/` 下的 `.puml` 文件（用例图、领域类图、包图、设计类图、3 张顺序图），用 PlantUML 渲染。

## 12. Agent 使用

本项目 Specs 与代码均由 Claude Code 辅助生成，人工审查后冻结 baseline，使用记录见 `specs/19-ai-usage-log.md`。
