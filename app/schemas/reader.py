"""读者与借阅证 DTO。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..domain.enums import CardStatus, ReaderType


class ReaderCreate(BaseModel):
    name: str
    department: str
    reader_type: ReaderType
    email: str | None = None
    phone: str | None = None


class ReaderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    department: str
    reader_type: ReaderType
    email: str | None = None
    phone: str | None = None


class BorrowCardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    card_no: str
    reader_id: int
    reader_name: str
    department: str
    status: CardStatus
    issued_at: datetime
    cancelled_at: datetime | None = None


class IssueCardRequest(BaseModel):
    reader_id: int
