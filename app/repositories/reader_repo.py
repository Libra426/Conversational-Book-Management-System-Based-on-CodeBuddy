"""读者与借阅证仓储。"""
from sqlalchemy.orm import Session, joinedload

from ..domain.enums import CardStatus
from ..domain.models import BorrowCard, Reader


class ReaderRepo:
    def __init__(self, db: Session):
        self.db = db

    def get(self, reader_id: int) -> Reader | None:
        return self.db.get(Reader, reader_id)

    def list_all(self) -> list[Reader]:
        return self.db.query(Reader).order_by(Reader.id).all()

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

    def list_all(self) -> list[BorrowCard]:
        return (
            self.db.query(BorrowCard)
            .options(joinedload(BorrowCard.reader))
            .order_by(BorrowCard.id)
            .all()
        )

    def create(self, card: BorrowCard) -> BorrowCard:
        self.db.add(card)
        self.db.flush()
        return card

    def max_sequence_for_year(self, year: int) -> int:
        """返回某年份已发放借阅证的最大 6 位序号（用于生成下一个证号）。"""
        prefix = f"CARD{year}"
        rows = (
            self.db.query(BorrowCard.card_no)
            .filter(BorrowCard.card_no.like(prefix + "%"))
            .all()
        )
        max_seq = 0
        for (card_no,) in rows:
            suffix = card_no[len(prefix):]
            if suffix.isdigit():
                max_seq = max(max_seq, int(suffix))
        return max_seq
