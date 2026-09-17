"""读者与借阅证仓储。"""
from sqlalchemy.orm import Session

from ..domain.enums import CardStatus
from ..domain.models import BorrowCard, Reader


class ReaderRepo:
    def __init__(self, db: Session):
        self.db = db

    def get(self, reader_id: int) -> Reader | None:
        return self.db.get(Reader, reader_id)

    def create(self, reader: Reader) -> Reader:
        self.db.add(reader)
        self.db.flush()
        return reader


class BorrowCardRepo:
    def __init__(self, db: Session):
        self.db = db

    def find_active_by_card_no(self, card_no: str) -> BorrowCard | None:
        return (
            self.db.query(BorrowCard)
            .filter(BorrowCard.card_no == card_no, BorrowCard.status == CardStatus.ACTIVE)
            .first()
        )

    def find_active_by_reader(self, reader_id: int) -> BorrowCard | None:
        return (
            self.db.query(BorrowCard)
            .filter(BorrowCard.reader_id == reader_id, BorrowCard.status == CardStatus.ACTIVE)
            .first()
        )

    def get_by_card_no(self, card_no: str) -> BorrowCard | None:
        return self.db.query(BorrowCard).filter(BorrowCard.card_no == card_no).first()

    def create(self, card: BorrowCard) -> BorrowCard:
        self.db.add(card)
        self.db.flush()
        return card

    def count(self) -> int:
        return self.db.query(BorrowCard).count()
