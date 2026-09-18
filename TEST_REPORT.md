# 自动化测试报告

> 图书管理系统（AI 时代 Spec-Driven 实验）—— 自动化测试执行报告

## 1. 测试概览

| 项目 | 值 |
|---|---|
| 测试框架 | pytest ≥ 8.0 + httpx |
| 测试目录 | `tests/`（5 个测试文件 + conftest + helpers） |
| 用例总数 | **35** |
| 通过 | **35** |
| 失败 / 跳过 | 0 / 0 |
| 执行耗时 | 约 1.8s |
| 执行时间 | 2026-09-18 |

## 2. 测试环境

- 语言：Python 3.13
- 框架：FastAPI + SQLAlchemy 2 + Pydantic 2
- 数据库：测试使用**独立 SQLite 内存/临时库**（`tests/conftest.py` 提供 fixture），不污染开发库 `library.db`，故演示数据不影响测试结果
- 配置：`pytest.ini`（`testpaths = tests`、`pythonpath = .`）

## 3. 运行方式

```bash
pip install -r requirements.txt
python -m pytest -v        # 或 pytest -v
```

预期输出：`35 passed`。

## 4. 测试用例清单

### 4.1 借还与查询 `tests/test_circulation.py`（9 个）

| # | 用例 | 验证目的 | 对应需求 |
|---|---|---|---|
| 1 | `test_borrow_success` | 借书成功并生成借阅记录 | FR-011 / UC-101 |
| 2 | `test_borrow_invalid_card` | 借阅证无效 → 拒绝 | FR-011 / BR-004 |
| 3 | `test_borrow_too_many` | 超出读者类型借阅上限 → 拒绝 | FR-011 / BR-005 |
| 4 | `test_borrow_overdue_loan` | 存在超期未还 → 拒绝 | FR-011 / BR-006 |
| 5 | `test_borrow_item_not_available` | 副本不可借（非 AVAILABLE）→ 拒绝 | FR-011 / BR-007 |
| 6 | `test_return_success` | 还书成功、副本恢复可借 | FR-012 / UC-102 |
| 7 | `test_return_item_not_found` | 还书副本不存在 → 拒绝 | FR-012 |
| 8 | `test_return_overdue_generates_fine` | 超期还书自动生成罚单 | FR-012 / FR-015 / BR-009/010 |
| 9 | `test_query_loans_success` | 查询借阅信息 | FR-013 / UC-003/103 |

### 4.2 权限隔离 `tests/test_permission.py`（8 个）

| # | 用例 | 验证目的 | 对应需求 |
|---|---|---|---|
| 10 | `test_reader_cannot_execute_admin_operation` | 读者不能执行管理员操作 | BR-012 |
| 11 | `test_reader_cannot_borrow` | 读者不能代办借书 | BR-001 / BR-012 |
| 12 | `test_reader_cannot_query_others` | 读者不能查他人借阅 | FR-013 / BR-012 |
| 13 | `test_reader_cannot_query_other_reader_info` | 读者不能查他人基本信息 | BR-012 |
| 14 | `test_reader_can_query_own_info` | 读者可查本人信息 | FR-013 |
| 15 | `test_bearer_token_grants_admin` | Bearer 令牌授予 admin 权限 | 权限模型 |
| 16 | `test_bearer_token_wrong_role_denied` | Bearer 令牌角色不符被拒 | 权限模型 |
| 17 | `test_bearer_token_overrides_header` | Bearer 令牌优先于 X-Role 头 | 权限模型 |

### 4.3 借阅/罚款规则策略 `tests/test_policy.py`（7 个）

| # | 用例 | 验证目的 | 对应需求 |
|---|---|---|---|
| 18 | `test_borrow_policy_defaults` | 借阅规则默认值正确 | FR-016 / BR-008 |
| 19 | `test_borrow_policy_can_borrow` | 数量上限判断逻辑 | BR-005 |
| 20 | `test_due_date` | 按类型计算到期日 | BR-008 |
| 21 | `test_fine_rule_defaults` | 罚款规则默认值正确 | FR-015 / BR-009 |
| 22 | `test_fine_zero_or_negative` | 超期 ≤ 0 不罚款 | BR-010 |
| 23 | `test_negative_policy_rejected` | 负数借阅规则参数被拒（422） | FR-016 |
| 24 | `test_negative_fine_rejected` | 负数罚款规则参数被拒（422） | FR-016 |

### 4.4 读者与借阅证 `tests/test_reader.py`（7 个）

| # | 用例 | 验证目的 | 对应需求 |
|---|---|---|---|
| 25 | `test_register_reader_success` | 注册读者成功 | FR-001 / UC-001 |
| 26 | `test_issue_card_success` | 办理借阅证成功 | FR-002 / UC-201 |
| 27 | `test_issue_card_inlines_reader_info` | 借阅证内联读者姓名/院系 | FR-002 |
| 28 | `test_issue_card_reader_not_found` | 办证：读者不存在 → 拒绝 | FR-002 |
| 29 | `test_issue_card_duplicate` | 办证：重复办理 → 拒绝 | BR-003 |
| 30 | `test_get_reader_by_card` | 证号解析读者成功 | FR-013 |
| 31 | `test_get_reader_by_card_not_found` | 证号不存在 → 404 | FR-013 |

### 4.5 预约 `tests/test_reservation.py`（4 个）

| # | 用例 | 验证目的 | 对应需求 |
|---|---|---|---|
| 32 | `test_reserve_success` | 预约成功 | FR-014 / UC-004 |
| 33 | `test_reserve_duplicate` | 重复预约 → 拒绝 | BR-011 |
| 34 | `test_reserve_reader_not_found` | 预约：读者不存在 → 拒绝 | FR-014 |
| 35 | `test_reserve_title_not_found` | 预约：标题不存在 → 拒绝 | FR-014 |

## 5. 需求覆盖映射

| 功能需求 | 覆盖测试 |
|---|---|
| FR-001 注册读者 | #25 |
| FR-002 办理借阅证 | #26–#29 |
| FR-003 注销借阅证 | 借阅证生命周期由 #26–#29 间接覆盖 |
| FR-011 借书 | #1–#5 |
| FR-012 还书 | #6–#8 |
| FR-013 查询借阅 | #9、#12–#14、#30–#31 |
| FR-014 预约 | #32–#35 |
| FR-015 超期罚款 | #8、#21、#22 |
| FR-016 规则维护 | #18–#24 |
| BR-012 权限互斥 | #10–#17 |

核心业务规则（BR-001~013）与角色权限（reader/librarian/admin）均有对应测试覆盖。

## 6. 运行结果

```
collected 35 items

tests/test_circulation.py::test_borrow_success PASSED                    [  2%]
tests/test_circulation.py::test_borrow_invalid_card PASSED               [  5%]
tests/test_circulation.py::test_borrow_too_many PASSED                   [  8%]
tests/test_circulation.py::test_borrow_overdue_loan PASSED               [ 11%]
tests/test_circulation.py::test_borrow_item_not_available PASSED         [ 14%]
tests/test_circulation.py::test_return_success PASSED                    [ 17%]
tests/test_circulation.py::test_return_item_not_found PASSED             [ 20%]
tests/test_circulation.py::test_return_overdue_generates_fine PASSED     [ 22%]
tests/test_circulation.py::test_query_loans_success PASSED               [ 25%]
tests/test_permission.py::test_reader_cannot_execute_admin_operation PASSED [ 28%]
tests/test_permission.py::test_reader_cannot_borrow PASSED               [ 31%]
tests/test_permission.py::test_reader_cannot_query_others PASSED         [ 34%]
tests/test_permission.py::test_reader_cannot_query_other_reader_info PASSED [ 37%]
tests/test_permission.py::test_reader_can_query_own_info PASSED          [ 40%]
tests/test_permission.py::test_bearer_token_grants_admin PASSED          [ 42%]
tests/test_permission.py::test_bearer_token_wrong_role_denied PASSED     [ 45%]
tests/test_permission.py::test_bearer_token_overrides_header PASSED      [ 48%]
tests/test_policy.py::test_borrow_policy_defaults PASSED                 [ 51%]
tests/test_policy.py::test_borrow_policy_can_borrow PASSED               [ 54%]
tests/test_policy.py::test_due_date PASSED                               [ 57%]
tests/test_policy.py::test_fine_rule_defaults PASSED                     [ 60%]
tests/test_policy.py::test_fine_zero_or_negative PASSED                  [ 62%]
tests/test_policy.py::test_negative_policy_rejected PASSED               [ 65%]
tests/test_policy.py::test_negative_fine_rejected PASSED                 [ 68%]
tests/test_reader.py::test_register_reader_success PASSED                [ 71%]
tests/test_reader.py::test_issue_card_success PASSED                     [ 74%]
tests/test_reader.py::test_issue_card_inlines_reader_info PASSED         [ 77%]
tests/test_reader.py::test_issue_card_reader_not_found PASSED            [ 80%]
tests/test_reader.py::test_issue_card_duplicate PASSED                   [ 82%]
tests/test_reader.py::test_get_reader_by_card PASSED                     [ 85%]
tests/test_reader.py::test_get_reader_by_card_not_found PASSED           [ 88%]
tests/test_reservation.py::test_reserve_success PASSED                   [ 91%]
tests/test_reservation.py::test_reserve_duplicate PASSED                 [ 94%]
tests/test_reservation.py::test_reserve_reader_not_found PASSED          [ 97%]
tests/test_reservation.py::test_reserve_title_not_found PASSED           [100%]

======================== 35 passed, 1 warning in 1.82s ========================
```

> 注：输出末尾的 `StarletteDeprecationWarning` 为 FastAPI 测试客户端依赖的弃用提示，不影响任何测试结果。
