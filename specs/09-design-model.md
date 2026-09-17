# 详细设计模型

以用例为单元，说明每个用例涉及的类、职责、异常与事务边界。

## 1. 办理借书（UC-101）

| 元素 | 类 | 职责 |
|---|---|---|
| Controller | `CirculationRouter.borrow` | 接收 BorrowRequest，返回 LoanOut |
| Application Service | `CirculationService.borrow()` | 编排校验流程，事务边界 |
| 策略 | `BorrowPolicyService` | 校验数量、计算 due_date |
| Repository | `BorrowCardRepo`、`LoanRepo`、`LibraryItemRepo` | 持久化读写 |
| Entity | `Reader`、`BorrowCard`、`LibraryItem`、`Loan` | 领域对象 |
| DTO | `BorrowRequest`、`LoanOut` | 入参/出参 |
| 异常 | `InvalidCardError`、`TooManyLoansError`、`OverdueLoanError`、`ItemNotBorrowableError` | 分支失败 |

流程：借阅证有效 → 未超数量 → 无超期未还 → 副本可借 → 创建 Loan + 副本置 BORROWED。

## 2. 办理还书（UC-102）

| 元素 | 类 | 职责 |
|---|---|---|
| Controller | `CirculationRouter.return_book` | 接收条码，返回 ReturnOut |
| Application Service | `CirculationService.return_book()` | 编排还书与罚款 |
| 策略 | `FineService` | 计算罚款 |
| Repository | `LibraryItemRepo`、`LoanRepo`、`FineRecordRepo` | 读写 |
| Entity | `LibraryItem`、`Loan`、`FineRecord` | 领域对象 |
| 异常 | `ItemNotFoundError`、`LoanNotFoundError` | 分支失败 |

流程：副本存在 → 找未还 Loan → 置 RETURNED + 副本 AVAILABLE → 超期则生成罚单。

## 3. 预约图书（UC-004）

| 元素 | 类 | 职责 |
|---|---|---|
| Controller | `ReservationRouter.create` | 接收 ReservationRequest |
| Application Service | `ReservationService.reserve()` | 校验 + 排队 |
| Repository | `ReaderRepo`、`BookTitleRepo`、`ReservationRepo` | 读写 |
| Entity | `Reader`、`BookTitle`、`Reservation` | 领域对象 |
| 异常 | `ReaderNotFoundError`、`TitleNotFoundError`、`DuplicateReservationError` | 分支失败 |

## 4. 查询借阅信息（UC-003）

| 元素 | 类 | 职责 |
|---|---|---|
| Controller | `CirculationRouter.query_loans` | 接收 reader_id |
| Application Service | `CirculationService.query_loans()` | 权限判断（本人/管理员） |
| Repository | `LoanRepo` | 查询 |
| 异常 | `PermissionDeniedError` | 越权 |

## 5. 办理借阅证（UC-201）

| 元素 | 类 | 职责 |
|---|---|---|
| Controller | `AdminRouter.issue_card` | 接收 reader_id |
| Application Service | `ReaderService.issue_card()` | 生成唯一卡号 + 建卡 |
| Repository | `ReaderRepo`、`BorrowCardRepo` | 读写 |
| 异常 | `ReaderNotFoundError`、`DuplicateCardError` | 分支失败 |

## 6. 添加图书标题/馆藏副本（UC-205/207）

| 元素 | 类 | 职责 |
|---|---|---|
| Controller | `AdminRouter.add_title` / `add_item` | 接收入参 |
| Application Service | `CatalogService` | 创建标题/副本 |
| Repository | `BookTitleRepo`、`LibraryItemRepo` | 读写 |
| 异常 | `DuplicateIsbnError`、`DuplicateBarcodeError`、`TitleNotFoundError` | 分支失败 |

## 7. 设计模式落点

- Strategy：`BorrowPolicy`（按 reader_type）、`FineRule`（按 item_type）。
- Repository：`app/repositories/*`。
- Service Layer：`app/services/*`。
- DTO：`app/schemas/*`。

## 8. 事务边界

- 借书：读规则/读证/读副本/写 Loan/写副本，同一会话提交。
- 还书：写 Loan/写副本/写 FineRecord，同一会话提交。
- 办证：生成卡号/写 BorrowCard，同一会话提交。
