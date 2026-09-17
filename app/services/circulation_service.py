"""借还与借阅查询应用服务。"""
from datetime import date, datetime

from sqlalchemy.orm import Session

from ..domain.enums import ItemStatus, LoanStatus
from ..domain.models import FineRecord, Loan
from ..exceptions import (
    InvalidCardError,
    ItemNotBorrowableError,
    ItemNotFoundError,
    LoanNotFoundError,
    OverdueLoanError,
    PermissionDeniedError,
    TooManyLoansError,
)
from ..repositories.circulation_repo import FineRecordRepo, LoanRepo
from ..repositories.catalog_repo import LibraryItemRepo
from ..repositories.reader_repo import BorrowCardRepo
from ..schemas.circulation import BorrowRequest, ReturnRequest
from .fine_service import FineService
from .policy_service import BorrowPolicyService


class CirculationService:
    def __init__(self, db: Session):
        self.db = db
        self.card_repo = BorrowCardRepo(db)
        self.loan_repo = LoanRepo(db)
        self.item_repo = LibraryItemRepo(db)
        self.fine_repo = FineRecordRepo(db)
        self.policy_svc = BorrowPolicyService(db)
        self.fine_svc = FineService(db)

    def borrow(self, data: BorrowRequest) -> Loan:
        card = self.card_repo.find_active_by_card_no(data.card_no)
        if card is None:
            raise InvalidCardError("借阅证无效")

        reader = card.reader
        current = self.loan_repo.count_active_by_reader(reader.id)
        if not self.policy_svc.can_borrow(reader.reader_type, current):
            raise TooManyLoansError("超出借阅数量")
        if self.loan_repo.has_overdue_by_reader(reader.id, date.today()):
            raise OverdueLoanError("存在超期未还图书")

        item = self.item_repo.find_by_barcode(data.barcode)
        if item is None:
            raise ItemNotFoundError("非本馆藏书")
        if item.status != ItemStatus.AVAILABLE:
            raise ItemNotBorrowableError("图书不可借")

        loan = Loan(
            reader_id=reader.id,
            item_id=item.id,
            due_date=self.policy_svc.due_date(reader.reader_type),
            status=LoanStatus.BORROWED,
        )
        self.loan_repo.create(loan)
        item.status = ItemStatus.BORROWED
        self.db.commit()
        return loan

    def return_book(self, data: ReturnRequest) -> tuple[Loan, FineRecord | None]:
        item = self.item_repo.find_by_barcode(data.barcode)
        if item is None:
            raise ItemNotFoundError("非本馆藏书")

        loan = self.loan_repo.find_active_by_item(item.id)
        if loan is None:
            raise LoanNotFoundError("未找到借阅记录")

        now = datetime.now()
        loan.returned_at = now
        loan.status = LoanStatus.RETURNED
        item.status = ItemStatus.AVAILABLE

        fine_record = None
        overdue = self.fine_svc.overdue_days(loan.due_date, now.date())
        if overdue > 0:
            item_type = loan.item.title.item_type
            amount = self.fine_svc.calculate_fine(item_type, overdue)
            fine_record = self.fine_repo.create(
                FineRecord(loan_id=loan.id, overdue_days=overdue, amount=amount)
            )

        self.db.commit()
        return loan, fine_record

    def query_loans(self, reader_id: int, role: str, user_id: int) -> list[Loan]:
        if role not in ("librarian", "admin") and not (role == "reader" and user_id == reader_id):
            raise PermissionDeniedError("只能查询本人借阅信息")
        return self.loan_repo.list_by_reader(reader_id)
