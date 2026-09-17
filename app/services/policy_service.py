"""借阅规则策略（Strategy）：按读者类型提供数量与期限。"""
from datetime import date, timedelta

from sqlalchemy.orm import Session

from ..domain.enums import ReaderType
from ..domain.models import BorrowPolicy
from ..exceptions import PolicyNotFoundError
from ..schemas.admin import BorrowPolicyUpsert


class BorrowPolicyService:
    def __init__(self, db: Session):
        self.db = db

    def get_policy(self, reader_type: ReaderType) -> BorrowPolicy:
        policy = (
            self.db.query(BorrowPolicy)
            .filter(BorrowPolicy.reader_type == reader_type)
            .first()
        )
        if policy is None:
            raise PolicyNotFoundError(f"缺少读者类型 {reader_type} 的借阅规则")
        return policy

    def get_max_borrow_count(self, reader_type: ReaderType) -> int:
        return self.get_policy(reader_type).max_borrow_count

    def get_borrow_days(self, reader_type: ReaderType) -> int:
        return self.get_policy(reader_type).borrow_days

    def can_borrow(self, reader_type: ReaderType, current_count: int) -> bool:
        return self.get_policy(reader_type).can_borrow(current_count)

    def due_date(self, reader_type: ReaderType, borrowed_on: date | None = None) -> date:
        borrowed_on = borrowed_on or date.today()
        return borrowed_on + timedelta(days=self.get_borrow_days(reader_type))

    def list_all(self) -> list[BorrowPolicy]:
        return self.db.query(BorrowPolicy).order_by(BorrowPolicy.id).all()

    def upsert(self, data: BorrowPolicyUpsert) -> BorrowPolicy:
        policy = (
            self.db.query(BorrowPolicy)
            .filter(BorrowPolicy.reader_type == data.reader_type)
            .first()
        )
        if policy is None:
            policy = BorrowPolicy(reader_type=data.reader_type)
            self.db.add(policy)
        policy.max_borrow_count = data.max_borrow_count
        policy.borrow_days = data.borrow_days
        self.db.commit()
        return policy
