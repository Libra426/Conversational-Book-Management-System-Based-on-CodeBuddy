"""预约 DTO。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..domain.enums import ReservationStatus


class ReservationRequest(BaseModel):
    reader_id: int
    title_id: int


class ReservationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reader_id: int
    title_id: int
    status: ReservationStatus
    created_at: datetime
