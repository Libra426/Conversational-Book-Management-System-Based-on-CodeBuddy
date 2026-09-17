"""读者与借阅证应用服务。"""
from datetime import datetime

from sqlalchemy.orm import Session

from ..domain.enums import CardStatus
from ..domain.models import BorrowCard, Reader
from ..exceptions import (
    DuplicateCardError,
    NotFoundError,
    ReaderNotFoundError,
)
from ..repositories.reader_repo import BorrowCardRepo, ReaderRepo
from ..schemas.reader import ReaderCreate


class ReaderService:
    def __init__(self, db: Session):
        self.db = db
        self.reader_repo = ReaderRepo(db)
        self.card_repo = BorrowCardRepo(db)

    def register(self, data: ReaderCreate) -> Reader:
        reader = Reader(
            name=data.name,
            department=data.department,
            reader_type=data.reader_type,
            email=data.email,
            phone=data.phone,
        )
        self.reader_repo.create(reader)
        self.db.commit()
        return reader

    def get_reader(self, reader_id: int) -> Reader:
        reader = self.reader_repo.get(reader_id)
        if reader is None:
            raise ReaderNotFoundError("读者不存在")
        return reader

    def issue_card(self, reader_id: int) -> BorrowCard:
        reader = self.reader_repo.get(reader_id)
        if reader is None:
            raise ReaderNotFoundError("读者不存在")
        if self.card_repo.find_active_by_reader(reader_id) is not None:
            raise DuplicateCardError("该读者已有有效借阅证")
        card = BorrowCard(
            card_no=self._generate_card_no(),
            reader_id=reader_id,
            status=CardStatus.ACTIVE,
        )
        card.reader = reader  # 预挂载读者，供返回时内联姓名/院系
        self.card_repo.create(card)
        self.db.commit()
        return card

    def revoke_card(self, card_no: str) -> BorrowCard:
        card = self.card_repo.get_by_card_no(card_no)
        if card is None:
            raise NotFoundError("借阅证不存在")
        card.status = CardStatus.CANCELLED
        card.cancelled_at = datetime.now()
        _ = card.reader  # 预加载读者，供返回时内联姓名/院系
        self.db.commit()
        return card

    def _generate_card_no(self) -> str:
        seq = self.card_repo.count() + 1
        return str(seq)
