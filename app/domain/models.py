"""领域实体：SQLAlchemy 映射 + 领域行为。

继承映射策略：Reader 子类型用 reader_type 判别，LibraryItem 子类型用 item_type 判别（单表继承）。
"""
from datetime import date, datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from ..database import Base
from .enums import (
    CardStatus,
    FineStatus,
    ItemStatus,
    ItemType,
    LoanStatus,
    ReaderType,
    ReservationStatus,
)


def _now() -> datetime:
    return datetime.now()


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)
    reader_type = Column(Enum(ReaderType), nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    created_at = Column(DateTime, default=_now)

    borrow_card = relationship("BorrowCard", back_populates="reader", uselist=False)
    loans = relationship("Loan", back_populates="reader")
    reservations = relationship("Reservation", back_populates="reader")


class BorrowCard(Base):
    __tablename__ = "borrow_cards"

    id = Column(Integer, primary_key=True, index=True)
    card_no = Column(String, unique=True, nullable=False, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    status = Column(Enum(CardStatus), default=CardStatus.ACTIVE, nullable=False)
    issued_at = Column(DateTime, default=_now)
    cancelled_at = Column(DateTime, nullable=True)

    reader = relationship("Reader", back_populates="borrow_card")

    @property
    def reader_name(self) -> str:
        return self.reader.name

    @property
    def department(self) -> str:
        return self.reader.department


class Librarian(Base):
    __tablename__ = "librarians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class SystemAdmin(Base):
    __tablename__ = "system_admins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class BookTitle(Base):
    __tablename__ = "book_titles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False, index=True)
    publisher = Column(String, nullable=True)
    item_type = Column(Enum(ItemType), nullable=False)

    items = relationship("LibraryItem", back_populates="title")
    reservations = relationship("Reservation", back_populates="title")

    @property
    def total_count(self) -> int:
        return len(self.items)

    @property
    def available_count(self) -> int:
        return sum(1 for i in self.items if i.status == ItemStatus.AVAILABLE)


class LibraryItem(Base):
    __tablename__ = "library_items"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, unique=True, nullable=False, index=True)
    title_id = Column(Integer, ForeignKey("book_titles.id"), nullable=False)
    status = Column(Enum(ItemStatus), default=ItemStatus.AVAILABLE, nullable=False)

    title = relationship("BookTitle", back_populates="items")
    loans = relationship("Loan", back_populates="item")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("library_items.id"), nullable=False)
    borrowed_at = Column(DateTime, default=_now)
    due_date = Column(Date, nullable=False)
    returned_at = Column(DateTime, nullable=True)
    status = Column(Enum(LoanStatus), default=LoanStatus.BORROWED, nullable=False)

    reader = relationship("Reader", back_populates="loans")
    item = relationship("LibraryItem", back_populates="loans")
    fine_records = relationship("FineRecord", back_populates="loan")

    def is_overdue(self, today: date | None = None) -> bool:
        if self.status != LoanStatus.BORROWED:
            return False
        today = today or date.today()
        return self.due_date < today

    # 面向前端展示的内联字段：借阅的书籍/条码信息。
    @property
    def barcode(self) -> str:
        return self.item.barcode

    @property
    def title(self) -> str:
        return self.item.title.title

    @property
    def author(self) -> str:
        return self.item.title.author

    @property
    def item_type(self) -> ItemType:
        return self.item.title.item_type


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    title_id = Column(Integer, ForeignKey("book_titles.id"), nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, default=_now)

    reader = relationship("Reader", back_populates="reservations")
    title = relationship("BookTitle", back_populates="reservations")

    # 面向前端展示的内联字段：预约的书籍信息（title 关系名已占用，故用 book_title）。
    @property
    def book_title(self) -> str:
        return self.title.title

    @property
    def author(self) -> str:
        return self.title.author

    @property
    def item_type(self) -> ItemType:
        return self.title.item_type


class BorrowPolicy(Base):
    __tablename__ = "borrow_policies"

    id = Column(Integer, primary_key=True)
    reader_type = Column(Enum(ReaderType), unique=True, nullable=False)
    max_borrow_count = Column(Integer, nullable=False)
    borrow_days = Column(Integer, nullable=False)

    def can_borrow(self, current_count: int) -> bool:
        return current_count < self.max_borrow_count


class FineRule(Base):
    __tablename__ = "fine_rules"

    id = Column(Integer, primary_key=True)
    item_type = Column(Enum(ItemType), unique=True, nullable=False)
    fine_per_day = Column(Float, nullable=False)

    def calculate(self, overdue_days: int) -> float:
        if overdue_days <= 0:
            return 0.0
        return round(overdue_days * self.fine_per_day, 2)


class FineRecord(Base):
    __tablename__ = "fine_records"

    id = Column(Integer, primary_key=True, index=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    overdue_days = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(Enum(FineStatus), default=FineStatus.UNPAID, nullable=False)
    created_at = Column(DateTime, default=_now)

    loan = relationship("Loan", back_populates="fine_records")
