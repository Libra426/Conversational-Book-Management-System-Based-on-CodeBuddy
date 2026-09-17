"""借阅与罚单仓储。"""
from datetime import date

from sqlalchemy.orm import Session

from ..domain.enums import LoanStatus
from ..domain.models import FineRecord, Loan


class LoanRepo:
    def __init__(self, db: Session):
        self.db = db

    def count_active_by_reader(self, reader_id: int) -> int:
        return (
            self.db.query(Loan)
            .filter(Loan.reader_id == reader_id, Loan.status == LoanStatus.BORROWED)
            .count()
        )

    def has_overdue_by_reader(self, reader_id: int, today: date) -> bool:
        return (
            self.db.query(Loan)
            .filter(
                Loan.reader_id == reader_id,
                Loan.status == LoanStatus.BORROWED,
                Loan.due_date < today,
            )
            .count()
            > 0
        )

    def find_active_by_item(self, item_id: int) -> Loan | None:
        return (
            self.db.query(Loan)
            .filter(Loan.item_id == item_id, Loan.status == LoanStatus.BORROWED)
            .first()
        )

    def list_by_reader(self, reader_id: int) -> list[Loan]:
        return (
            self.db.query(Loan)
            .filter(Loan.reader_id == reader_id)
            .order_by(Loan.borrowed_at.desc())
            .all()
        )

    def create(self, loan: Loan) -> Loan:
        self.db.add(loan)
        self.db.flush()
        return loan


class FineRecordRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, record: FineRecord) -> FineRecord:
        self.db.add(record)
        self.db.flush()
        return record
