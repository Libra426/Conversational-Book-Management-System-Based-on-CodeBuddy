"""借还 DTO。"""
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from ..domain.enums import LoanStatus


class BorrowRequest(BaseModel):
    card_no: str
    barcode: str


class ReturnRequest(BaseModel):
    barcode: str


class FineOut(BaseModel):
    overdue_days: int
    amount: float


class LoanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reader_id: int
    item_id: int
    borrowed_at: datetime
    due_date: date
    returned_at: datetime | None = None
    status: LoanStatus


class ReturnOut(BaseModel):
    loan_id: int
    returned_at: datetime
    fine: FineOut | None = None
