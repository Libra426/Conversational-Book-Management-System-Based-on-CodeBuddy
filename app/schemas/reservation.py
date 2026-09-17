"""预约 DTO。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..domain.enums import ItemType, ReservationStatus


class ReservationRequest(BaseModel):
    reader_id: int
    title_id: int


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reader_id: int
    title_id: int
    book_title: str
    author: str
    item_type: ItemType
    status: ReservationStatus
    created_at: datetime
