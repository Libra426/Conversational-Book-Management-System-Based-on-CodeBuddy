# 图书管理系统（AI 时代 Spec-Driven 实验）

> 《软件设计与体系结构》课程实验：图书管理系统的 Spec-Driven 架构设计、详细设计与 Agent 辅助实现。
>
> **验收状态**：✅ 全部 **35 个自动化测试通过**；交付物与《实验指导书》要求逐条对应（见「交付物清单」）。

## 1. 项目概述

本系统面向**读者 / 图书管理员 / 系统管理员**三类角色，覆盖读者注册、借阅证办理/注销、图书题名与馆藏副本管理、借书/还书（含超期罚款）、借阅查询、图书预约、借阅与罚款规则维护等完整业务闭环。

项目遵循 **Spec-Driven 开发流程**：先产出 22 份规格文档与 7 张 UML 图并冻结，再据此实现代码与自动化测试，全程由 Claude Code 辅助（过程记录见 [`specs/19-ai-usage-log.md`](specs/19-ai-usage-log.md)）。

## 2. 技术栈

| 类别 | 技术 | 说明 |
|---|---|---|
| 语言 | Python 3.13 | — |
| Web 框架 | FastAPI | 自动生成 OpenAPI 交互文档（`/docs`） |
| ORM | SQLAlchemy 2 | 对象关系映射 |
| 数据库 | SQLite | 开箱即用，首次启动自动建表 + 种子数据 |
| 数据校验 | Pydantic 2 | 请求/响应 DTO |
| 测试 | pytest + httpx | 35 个自动化测试 |

依赖清单见 [`requirements.txt`](requirements.txt)。

## 3. 架构设计

采用**分层架构（Layered Architecture）+ MVC**，业务规则不进入 Controller：

```
表现层 presentation   app/routers        HTTP 路由 + 权限校验（Controller）
        ↓ 调用
应用层 application    app/services       用例编排、事务边界（Service Layer）
        ↓ 调用                ↕
领域层 domain          app/domain        实体 / 枚举 / 策略
基础设施层 infrastructure  app/repositories + database   持久化访问
```

DTO（`app/schemas`）在表现层与应用层之间传输，隔离领域实体与外部接口。

### 设计模式

| 模式 | 落点 | 说明 |
|---|---|---|
| **Strategy 策略** | `BorrowPolicyService` / `FineService` | 按读者类型 / 借出物类型动态选择规则 |
| **Repository 仓储** | `app/repositories/*` | 隔离领域逻辑与持久化 |
| **Service Layer 服务层** | `app/services/*` | 用例编排与事务 |
| **DTO 隔离** | `app/schemas/*` | 请求/响应与领域实体解耦 |
| **MVC** | routers(Controller) + services/domain(Model) + static(View) | 前后端可拆分 |
| **单表继承** | `reader_type` / `item_type` 判别字段 | Student/Teacher、5 种借出物类型 |
| **依赖注入** | FastAPI `Depends` | `get_db` / `get_identity` |

## 4. 目录结构

```
library-management-ai/
├─ specs/                    # 22 份编号文档（00–21）+ 开发宪法
│   ├─ 00–03,05,07,09,13–19,21  .md   # 需求/用例/领域/架构/数据库/API/测试计划等
│   ├─ 04,06,08,10,11,12,20   .puml   # 用例图/领域类图/包图/顺序图×3/设计类图（已渲染 .png）
│   └─ constitution.md               # 开发宪法（Agent 行为准则）
├─ app/
│   ├─ main.py                # FastAPI 入口
│   ├─ database.py            # SQLAlchemy 引擎 / 会话
│   ├─ deps.py                # 权限依赖（get_identity / require_role）
│   ├─ exceptions.py          # 领域异常 → HTTP 状态码映射
│   ├─ seed.py                # 建表 + 规则种子 + 演示数据（幂等）
│   ├─ routers/               # 表现层（Controller）
│   ├─ services/              # 应用服务层
│   ├─ domain/                # 领域实体 + 枚举 + 策略
│   ├─ repositories/          # 基础设施层（持久化）
│   └─ schemas/               # DTO
├─ tests/                     # pytest 自动化测试（35 个）
├─ static/                    # 前端（原生 HTML/CSS/JS 单页应用）
├─ requirements.txt
└─ README.md
```

## 5. 快速开始

```bash
pip install -r requirements.txt

# 方式一：直接运行（推荐）
python app\main.py

# 方式二：uvicorn
uvicorn app.main:app --reload
```

- 交互式 API 文档：<http://127.0.0.1:8000/docs>
- 前端页面：<http://127.0.0.1:8000/>

首次启动自动建表并写入规则种子与演示数据，无需手工初始化数据库。

## 6. 权限模型

通过请求头表达操作人：

| 头 | 取值 | 说明 |
|---|---|---|
| `X-Role` | `reader` / `librarian` / `admin` | 操作角色 |
| `X-User-Id` | 操作人 id | 读者为内部 id（借阅证号对外） |

`/docs` 中更简单：点右上角 **Authorize**，粘贴角色（`admin` / `librarian` / `reader`，可带用户 id 如 `admin:1`）即可全局生效。**Bearer 令牌优先于 `X-Role` 头**。

> **读者身份说明**：借阅证号（`card_no`）对外，读者内部 id（`reader_id`）仅作数据库主键。读者登录、查借阅、预约、借书均用借阅证号——前端用 `GET /api/readers/by-card/{card_no}` 把证号解析成内部 id，再携带 `X-User-Id` 调用后续接口。

## 7. 核心功能与用例

| 角色 | 功能 |
|---|---|
| **读者 Reader** | 注册账号、查询图书、查询本人借阅信息、预约图书 |
| **图书管理员 Librarian** | 办理借书、办理还书、查询任意读者借阅信息 |
| **系统管理员 SystemAdmin** | 办理/注销借阅证、维护标题/馆藏副本/管理员/借阅与罚款规则 |

用例编号与详情见 [`specs/03-use-cases.md`](specs/03-use-cases.md) 与 [`specs/04-use-case-model.puml`](specs/04-use-case-model.puml)。

## 8. API 概览

完整规范（含请求/响应示例与状态码）见 [`specs/14-api-spec.md`](specs/14-api-spec.md)，核心端点如下：

| 模块 | 端点 | 权限 |
|---|---|---|
| 读者与借阅证 | `POST /api/readers` 注册读者；`GET /api/readers` 读者列表 | 公开 / librarian·admin |
| | `GET /api/readers/by-card/{card_no}` 证号查读者；`GET /api/readers/{id}` 查读者 | 公开 / reader本人·librarian·admin |
| | `POST/GET/DELETE /api/admin/borrow-cards` 办理/列表/注销借阅证 | admin |
| 图书与馆藏 | `GET /api/catalog/books` 查询图书；`POST/DELETE /api/admin/book-titles` 标题增删 | 公开 / admin |
| | `POST/DELETE /api/admin/library-items` 副本增删 | admin |
| 借还与查询 | `POST /api/circulation/borrow` 借书；`POST /api/circulation/return` 还书 | librarian |
| | `GET /api/readers/{id}/loans` 查询借阅 | reader本人·librarian·admin |
| 预约 | `POST /api/reservations` 预约；`GET /api/readers/{id}/reservations` 查预约 | reader / reader本人·librarian·admin |
| 规则与人员 | `GET/POST /api/admin/borrow-policies`、`GET/POST /api/admin/fine-rules` | admin |
| | `GET/POST/DELETE /api/admin/librarians`、`GET/POST/DELETE /api/admin/system-admins` | admin |

## 9. 业务规则

**借阅规则**（按读者类型，Strategy 模式数据驱动）：

| 读者类型 | 上限（本） | 期限（天） |
|---|---|---|
| 专科生 | 3 | 30 |
| 本科生 | 5 | 30 |
| 研究生 | 10 | 60 |
| 博士生 | 15 | 90 |
| 教师 | 20 | 90 |

**罚款规则**（按借出物类型）：

| 借出物类型 | 罚款（元/天） |
|---|---|
| 中文图书 | 0.10 |
| 外文图书 | 0.20 |
| 中文杂志 | 0.05 |
| 外文杂志 | 0.10 |
| 论文 | 0.50 |

其余业务规则（借阅证号格式 `CARD+4位年份+6位序号`、超期天数计算、预约去重等）见 [`specs/02-requirements.md`](specs/02-requirements.md) 第 4 节（BR-001~013）。

## 10. 自动化测试

```bash
pytest -v                 # 或 python -m pytest -v
```

结果为 **35 passed**。测试用例分布：

| 测试文件 | 数量 | 覆盖内容 |
|---|---|---|
| `tests/test_circulation.py` | 9 | 借书成功/证无效/超限/有超期未还/副本不可借；还书成功/副本不存在/超期生成罚单；查询借阅 |
| `tests/test_permission.py` | 8 | 角色权限隔离（读者越权被拒）+ Bearer 令牌优先级 |
| `tests/test_reader.py` | 7 | 注册读者、办证（含内联姓名/院系）、重复办证、证号解析 |
| `tests/test_policy.py` | 7 | 借阅/罚款规则默认值、计算、非负校验 |
| `tests/test_reservation.py` | 4 | 预约成功/重复预约/读者不存在/标题不存在 |

测试计划见 [`specs/15-test-plan.md`](specs/15-test-plan.md)，任务拆解见 [`specs/16-tasks.md`](specs/16-tasks.md)。

## 11. UML 文档

| 图 | 文件 | 说明 |
|---|---|---|
| 用例图 | `specs/04-use-case-model.puml` | 三类参与者与 20 余个用例 |
| 领域类图 | `specs/06-domain-class-diagram.puml` | 实体 + 5 个状态枚举 + 关系 |
| 包图 | `specs/08-package-diagram.puml` | 分层包依赖 |
| 顺序图 ×3 | `specs/10/11/12-*.puml` | 借书 / 还书 / 预约 交互 |
| 设计类图 | `specs/20-design-class-diagram.puml` | 各层类/接口及其依赖（实验一·步骤4） |

`.puml` 源文件已渲染为同名 `.png`，可用 PlantUML 直接渲染。

## 12. 演示数据（开箱即用）

首次启动自动写入，可直接测试借还书：

| 借阅证号 | 读者 | 类型 | 上限 / 期限 |
|---|---|---|---|
| CARD2026000001 | 张三 | 本科生 | 5 本 / 30 天 |
| CARD2026000002 | 李四 | 研究生 | 10 本 / 60 天 |
| CARD2026000003 | 王五 | 教师 | 20 本 / 90 天 |

| 条码 | 书名 | 类型 |
|---|---|---|
| BC-1001 / BC-1002 / BC-1003 | 软件工程 | 中文图书 |
| BC-2001 / BC-2002 | 算法导论 | 外文图书 |
| BC-3001 | 计算机学报 | 中文杂志 |
| BC-4001 / BC-4002 | Nature | 外文杂志 |
| BC-5001 | 基于深度学习的图像识别研究 | 论文 |

在 `/docs` 右上角 Authorize 填 `librarian` 后：

- 借书：`POST /api/circulation/borrow` → `{"card_no": "CARD2026000001", "barcode": "BC-1001"}`
- 还书：`POST /api/circulation/return` → `{"barcode": "BC-1001"}`

超期还书会自动按类型生成罚款（如中文图书 0.10 元/天）。

## 13. 交付物清单

| 交付物 | 文件 | 状态 |
|---|---|---|
| 项目简介 | `specs/00-project-brief.md` | ✅ |
| 澄清问题 | `specs/01-clarifying-questions.md` | ✅ |
| 需求规格说明书 | `specs/02-requirements.md`（FR-001~016、BR-001~013） | ✅ |
| 用例模型 | `specs/03-use-cases.md` + `04-use-case-model.puml` | ✅ |
| 领域模型 | `specs/05-domain-model.md` + `06-domain-class-diagram.puml` | ✅ |
| 架构设计 | `specs/07-architecture.md` + `08-package-diagram.puml` | ✅ |
| 详细设计 | `specs/09-design-model.md` + `20-design-class-diagram.puml` | ✅ |
| 顺序图 | `specs/10/11/12-sequence-*.puml` | ✅ |
| 数据库设计 | `specs/13-database-design.md` | ✅ |
| API 规范 | `specs/14-api-spec.md` | ✅ |
| 测试计划 | `specs/15-test-plan.md` | ✅ |
| 任务拆解 | `specs/16-tasks.md` | ✅ |
| 风险分析 | `specs/17-risk-analysis.md` | ✅ |
| 审查清单 | `specs/18-review-checklist.md` | ✅ |
| AI 使用记录 | `specs/19-ai-usage-log.md` | ✅ |
| Git 提交历史 | `specs/21-git-history.md` | ✅ |
| 开发宪法 | `specs/constitution.md` | ✅ |
| 源代码 | `app/`（34 个 .py） | ✅ |
| 自动化测试 | `tests/`（35 个） | ✅ |
| 前端 | `static/` | ✅ |

## 14. Agent 使用记录

本项目 Specs 与代码均由 **Claude Code** 辅助生成，人工审查后冻结 baseline。使用记录见 [`specs/19-ai-usage-log.md`](specs/19-ai-usage-log.md)（共 9 次），Git 提交历史见 [`GIT_HISTORY.md`](GIT_HISTORY.md)。
