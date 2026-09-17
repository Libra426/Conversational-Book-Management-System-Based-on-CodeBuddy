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

    def get_reader_by_card(self, card_no: str) -> Reader:
        """读者用借阅证号登录：借阅证号 → 读者（仅有效证）。"""
        card = self.card_repo.find_active_by_card_no(card_no)
        if card is None:
            raise NotFoundError("借阅证不存在或已注销")
        return card.reader

    def list_readers(self) -> list[Reader]:
        return self.reader_repo.list_all()

    def list_cards(self) -> list[BorrowCard]:
        return self.card_repo.list_all()

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
        # BR-002：借阅证号格式 `CARD` + 4 位年份 + 6 位序号，全局唯一。
        year = datetime.now().year
        seq = self.card_repo.max_sequence_for_year(year) + 1
        return f"CARD{year}{seq:06d}"
