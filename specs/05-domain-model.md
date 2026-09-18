# 领域模型

## 1. 领域类总览

| 类 | 类型 | 职责 |
|---|---|---|
| Reader | 实体（聚合根） | 读者，含读者类型，派生借阅规则 |
| BorrowCard | 实体 | 借阅证，凭以借书 |
| BookTitle | 实体（聚合根） | 图书题名信息 |
| LibraryItem | 实体 | 具体馆藏副本，含条码与状态 |
| Loan | 实体 | 借阅记录，表达借出/归还/超期 |
| Reservation | 实体 | 预约，按时间排队 |
| BorrowPolicy | 策略/值对象 | 某读者类型的借阅数量与期限规则 |
| FineRule | 策略/值对象 | 某借出物类型的每日罚款规则 |
| FineRecord | 实体 | 罚单 |
| Librarian / SystemAdmin | 实体 | 管理员（权限角色） |

## 2. 各类详述

### Reader（实体，聚合根）

- 职责：标识读者身份与类型，作为借阅/预约的归属。
- 关键属性：id、name、department、reader_type（JUNIOR_COLLEGE/UNDERGRADUATE/GRADUATE/DOCTOR/TEACHER）、email、phone。
- 关键行为：`reader_type` 决定借阅规则（委托 BorrowPolicy）。
- 约束：id 唯一；reader_type 必填。
- 关系：1—1 BorrowCard；1—N Loan；1—N Reservation。
- 说明：Student/Teacher 通过 `reader_type` 判别字段表达（单表继承），对应关系库 `readers.reader_type`。

### BorrowCard（实体）

- 职责：读者借书的凭证。
- 关键属性：id、card_no（唯一）、reader_id、status（ACTIVE/CANCELLED）、issued_at。
- 约束：card_no 唯一；同一 reader 至多一个 ACTIVE。
- 关系：N—1 Reader。

### BookTitle（实体，聚合根）

- 职责：描述一本书的题名信息。
- 关键属性：id、title、author、isbn（唯一）、publisher、item_type。
- 关系：1—N LibraryItem。

### LibraryItem（实体）

- 职责：具体馆藏副本。
- 关键属性：id、barcode（唯一）、title_id、status（AVAILABLE/BORROWED/RESERVED/REMOVED）。
- 关系：N—1 BookTitle；1—N Loan。

### Loan（实体）

- 职责：记录一次借阅，表达状态与超期。
- 关键属性：id、reader_id、item_id、borrowed_at、due_date、returned_at、status（BORROWED/RETURNED）。
- 关键行为：`is_overdue(now)`。
- 约束：一个副本至多一个未归还 Loan。
- 关系：N—1 Reader；N—1 LibraryItem；1—N FineRecord。

### Reservation（实体）

- 职责：预约登记，按时间排队。
- 关键属性：id、reader_id、title_id、status（ACTIVE/FULFILLED/CANCELLED）、created_at。
- 约束：同一 reader + title 至多一个 ACTIVE。
- 关系：N—1 Reader；N—1 BookTitle。

### BorrowPolicy（策略/值对象）

- 职责：封装某读者类型的借阅规则。
- 关键属性：reader_type（唯一）、max_borrow_count、borrow_days。
- 关键行为：`can_borrow(current_count)`、`due_date(borrowed_at)`。

### FineRule（策略/值对象）

- 职责：封装某借出物类型的罚款规则。
- 关键属性：item_type（唯一）、fine_per_day。
- 关键行为：`calculate(overdue_days)`。

### FineRecord（实体）

- 职责：一张罚单。
- 关键属性：id、loan_id、overdue_days、amount、status（UNPAID/PAID）、created_at。
- 关系：N—1 Loan。

## 3. 分类说明

- 实体：Reader、BorrowCard、BookTitle、LibraryItem、Loan、Reservation、FineRecord、Librarian、SystemAdmin。
- 值对象/策略：BorrowPolicy、FineRule（数据驱动、可替换，对应 Strategy 模式）。
- 领域服务：CirculationService（组织借/还流程）、FineService（计算罚款）、ReservationService。

## 4. 关系小结

```
Reader 1 ── 1 BorrowCard
Reader 1 ── N Loan
Loan   N ── 1 LibraryItem
LibraryItem N ── 1 BookTitle
Reader 1 ── N Reservation
Reservation N ── 1 BookTitle
Loan   1 ── N FineRecord
ReaderType  1 ── 1 BorrowPolicy
ItemType    1 ── 1 FineRule
```
