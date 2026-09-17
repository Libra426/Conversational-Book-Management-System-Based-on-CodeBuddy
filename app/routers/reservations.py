"""预约路由。"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.reservation import ReservationOut, ReservationRequest
from ..services.reservation_service import ReservationService

router = APIRouter(prefix="/api", tags=["reservations"])


@router.post("/reservations", response_model=ReservationOut, status_code=201)
def reserve_book(data: ReservationRequest, db: Session = Depends(get_db)):
    return ReservationService(db).reserve(data)
