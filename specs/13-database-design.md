# 数据库设计

## 1. 继承映射策略

Reader 的子类型（专科生/本科生/研究生/博士生/教师）与 LibraryItem 的子类型（图书/杂志/论文）均采用**单表继承 + 判别字段**：
- `readers.reader_type`（JUNIOR_COLLEGE/UNDERGRADUATE/GRADUATE/DOCTOR/TEACHER）
- `book_titles.item_type`（CHINESE_BOOK/FOREIGN_BOOK/CHINESE_MAGAZINE/FOREIGN_MAGAZINE/THESIS）

## 2. 表结构

### readers

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| name | VARCHAR | 否 | | 姓名 |
| department | VARCHAR | 否 | | 院系/单位 |
| reader_type | VARCHAR | 否 | | 读者类型 |
| email | VARCHAR | 是 | | 邮箱 |
| phone | VARCHAR | 是 | | 电话 |
| created_at | DATETIME | 否 | 默认 now | 创建时间 |

### borrow_cards

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| card_no | VARCHAR | 否 | UNIQUE | 借阅证号 |
| reader_id | INTEGER | 否 | FK→readers.id | 所属读者 |
| status | VARCHAR | 否 | 默认 ACTIVE | ACTIVE/CANCELLED |
| issued_at | DATETIME | 否 | 默认 now | 发证时间 |
| cancelled_at | DATETIME | 是 | | 注销时间 |

### librarians

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| name | VARCHAR | 否 | | 姓名 |

### system_admins

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| name | VARCHAR | 否 | | 姓名 |

### book_titles

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| title | VARCHAR | 否 | | 书名 |
| author | VARCHAR | 否 | | 作者 |
| isbn | VARCHAR | 否 | UNIQUE | ISBN |
| publisher | VARCHAR | 是 | | 出版社 |
| item_type | VARCHAR | 否 | | 借出物类型 |

### library_items

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| barcode | VARCHAR | 否 | UNIQUE | 馆藏条码 |
| title_id | INTEGER | 否 | FK→book_titles.id | 所属标题 |
| status | VARCHAR | 否 | 默认 AVAILABLE | AVAILABLE/BORROWED/RESERVED/REMOVED |

### loans

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| reader_id | INTEGER | 否 | FK→readers.id | 读者 |
| item_id | INTEGER | 否 | FK→library_items.id | 副本 |
| borrowed_at | DATETIME | 否 | 默认 now | 借出时间 |
| due_date | DATE | 否 | | 应还日期 |
| returned_at | DATETIME | 是 | | 归还时间 |
| status | VARCHAR | 否 | 默认 BORROWED | BORROWED/RETURNED |

### reservations

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| reader_id | INTEGER | 否 | FK→readers.id | 读者 |
| title_id | INTEGER | 否 | FK→book_titles.id | 标题 |
| status | VARCHAR | 否 | 默认 ACTIVE | ACTIVE/FULFILLED/CANCELLED |
| created_at | DATETIME | 否 | 默认 now | 预约时间（排队依据） |

### borrow_policies

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| reader_type | VARCHAR | 否 | UNIQUE | 读者类型 |
| max_borrow_count | INTEGER | 否 | | 最大借阅数 |
| borrow_days | INTEGER | 否 | | 借阅期限（天） |

### fine_rules

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| item_type | VARCHAR | 否 | UNIQUE | 借出物类型 |
| fine_per_day | FLOAT | 否 | | 每日罚款额 |

### fine_records

| 字段 | 类型 | 空 | 键/约束 | 说明 |
|---|---|---|---|---|
| id | INTEGER | 否 | PK | 主键 |
| loan_id | INTEGER | 否 | FK→loans.id | 关联借阅 |
| overdue_days | INTEGER | 否 | | 超期天数 |
| amount | FLOAT | 否 | | 罚款金额 |
| status | VARCHAR | 否 | 默认 UNPAID | UNPAID/PAID |
| created_at | DATETIME | 否 | 默认 now | 生成时间 |

## 3. 索引设计

- 唯一索引：`borrow_cards.card_no`、`library_items.barcode`、`book_titles.isbn`、`borrow_policies.reader_type`、`fine_rules.item_type`。
- 查询索引：`loans.reader_id`、`loans.item_id`、`loans.status`、`reservations.reader_id`、`reservations.title_id`。

## 4. 关键约束复核

- `borrow_cards.card_no` 唯一 ✓
- `library_items.barcode` 唯一 ✓
- loans 通过 status + due_date 区分借出/已还/超期 ✓
- reservations 通过 created_at + status 支持排队 ✓
- fine_rules 按 item_type 区分罚款 ✓
- borrow_policies 按 reader_type 区分规则 ✓
- 必要外键已建立 ✓
